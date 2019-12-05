from random import shuffle

from urllib.parse import urlencode

from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView

from rest_framework.viewsets import ReadOnlyModelViewSet

from games.models import Game, Genre, StoreActivation
from games.serializers import SearchGameSerializer, SearchGameFilter

from users.forms import MailForm


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
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('slug')
        symbol = self.request.GET.get('query')

        if slug:
            qs = qs.filter(genre__slug=slug)
        elif symbol:
            qs = qs.filter(title__istartswith=symbol)

        return qs


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


class GamesFreeList(ListView):
    model = Game
    template_name = "games_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_free=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Игры даром',
            'section': 'Игры даром',
            'is_freelist': True,
        })
        return context


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
