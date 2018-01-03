from django.conf.urls import url
from pages.views import AgreementDoc, ReviewsPage, GuaranteePage


urlpatterns = [
    url(r'^agreement/$', AgreementDoc.as_view(), name='agreement'),
    url(r'^reviews/$', ReviewsPage.as_view(), name='reviews'),
    url(r'^guarantee/$', GuaranteePage.as_view(), name='guarantees'),
]
