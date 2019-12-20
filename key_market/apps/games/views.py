from functools import reduce
import operator

from random import shuffle

from urllib.parse import urlencode

from django.conf import settings
from django.db.models import Q, Func, Max, Min
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView

from rest_framework.viewsets import ReadOnlyModelViewSet

from games.forms import FilterForm
from games.models import Game, Genre, StoreActivation
from games.serializers import SearchGameSerializer, SearchGameFilter

from users.forms import MailForm


class Floor(Func):
    function = 'FLOOR'
    arity = 1


class Ceiling(Func):
    function = 'CEILING'
    arity = 1


class PageTitleMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        store = self.kwargs.get('store')
        symbol = self.request.GET.get('query')

        title = 'Игры'
        section = 'Игры'
        active_page = ''

        if slug:
            title = Genre.objects.get(slug=slug).title
            section = Genre.objects.get(slug=slug).title
            active_page = slug
        elif store:
            title = '%s ключи' % store.title()
            section = store.title
            active_page = store
        elif symbol:
            title = 'Игры на букву %s' % symbol.title()
            section = 'Игры на букву %s' % symbol.title()
            context['is_alphabet'] = True
            context['alphabet_symbol'] = symbol

        context.update({
            'page_title': title,
            'section': section,
            'active_page': active_page,
        })

        return context


class GamesList(PageTitleMixin, ListView):
    model = Game
    template_name = "games_list.html"
    paginate_by = 20

    def get_form(self, prices):
        request = self.request
        price_min = request.GET.get('price_min') or 0
        price_max = request.GET.get('price_max') or prices['price_max']
        genre = request.GET.getlist('genre')
        store = request.GET.getlist('store_activation')
        mode = request.GET.getlist('mode')

        form = FilterForm(initial={
            'price_min': price_min,
            'price_max': price_max,
            'genre': genre,
            'store_activation': store,
            'mode': mode,
        })
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prices = Game.objects.aggregate(
            price_min=Floor(Min('my_coast')),
            price_max=Ceiling(Max('my_coast')))

        context.update({
            'prices': prices,
            'filter_form': self.get_form(prices),
        })

        return context

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('slug')
        symbol = self.request.GET.get('query')

        if slug:
            qs = qs.filter(genre__slug=slug)
        elif symbol:
            qs = qs.filter(title__istartswith=symbol)

        genre_ids = self.request.GET.getlist('genre')
        mode_ids = self.request.GET.getlist('mode')
        store_ids = self.request.GET.getlist('store_activation')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')

        q_filters = []

        if genre_ids:
            q_filters.append(
                reduce(operator.or_, [Q(genre=id) for id in genre_ids]))

        if mode_ids:
            q_filters.append(
                reduce(operator.or_, [Q(mode=id) for id in mode_ids]))

        if store_ids:
            q_filters.append(
                reduce(operator.or_,
                       [Q(store_activation=id) for id in store_ids]))

        if any([price_min, price_max]):
            if all([price_min, price_max]):
                q_filters.append(Q(my_coast__gte=price_min) &
                                 Q(my_coast__lte=price_max))
            elif price_min:
                q_filters.append(Q(my_coast__gte=price_min))
            elif price_max:
                q_filters.append(Q(my_coast__lte=price_max))

        return qs.filter(*q_filters).distinct()


class GamesStoreList(PageTitleMixin, ListView):
    model = Game
    template_name = "games_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        store = self.kwargs.get('store')
        if store:
            stories = dict(StoreActivation.CHOICES)
            id = list(stories.keys())[list(stories.values()).index(store)]
            # test[test2.index('uplay')]
            qs = qs.filter(store_activation=id)
        return qs


class GamesDetail(DetailView):
    model = Game
    template_name = "games_detail.html"


class GamesOrder(DetailView):
    form_class = MailForm
    model = Game
    template_name = "games_order.html"

    def get_form_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form(self):
        return self.form_class(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        game = self.get_object()
        if form.is_valid():
            form.save()
            url = '{host}?{params}'.format(
                host=settings.DIGISELLER_OPLATA,
                params=urlencode({
                    'id_d': game.digiseller_id,
                    'curr': form.cleaned_data['payment'],
                    'lang': 'ru-RU',
                    'failpage': 'http://%s%s' % (request.get_host(),
                                                 game.get_absolute_url()),
                }),
            )
            return redirect(url)
        self.object = game
        return self.render_to_response(self.get_context_data(form=form))


class GamesLucky(TemplateView):
    model = Game
    template_name = "games_lucky.html"


class IndexPage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slides = list(Game.objects.filter(is_slide=True))
        shuffle(slides)
        context.update({
            'is_index': True,
            'slides': slides,
            'games_all': Game.objects.all(),
            'games_new_on_site': Game.objects.order_by('-date_created')[:25],
            'games_on_main_page': (Game.objects
                                   .order_by('-date_release')
                                   .filter(on_main_page=True)[:25]),

            'games_soon': (Game.objects
                           .order_by('-date_release')
                           .filter(is_soon=True)[:25]),
        })
        return context


class SearchGameViewSet(ReadOnlyModelViewSet):
    filter_class = SearchGameFilter
    queryset = Game.objects.all()
    serializer_class = SearchGameSerializer
