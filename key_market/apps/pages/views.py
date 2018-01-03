from django.views.generic.base import TemplateView

from games.utils import fetch_reviews


class AgreementDoc(TemplateView):
    template_name = "pages_agreement.html"


class GuaranteePage(TemplateView):
    template_name = "pages_guarantee.html"


class ReviewsPage(TemplateView):
    template_name = "pages_reviews.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'reviews': fetch_reviews(),
        })
        return context
