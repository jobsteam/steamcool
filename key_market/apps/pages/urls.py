from django.conf.urls import url
from pages.views import AgreementDoc, ReviewsPage, GuaranteePage, PaymentPage, InstructionPage, SupportPage


urlpatterns = [
    url(r'^agreement/$', AgreementDoc.as_view(), name='agreement'),
    url(r'^reviews/$', ReviewsPage.as_view(), name='reviews'),
    url(r'^guarantee/$', GuaranteePage.as_view(), name='guarantees'),
    url(r'^payment/$', PaymentPage.as_view(), name='payment'),
    url(r'^instruction/$', InstructionPage.as_view(), name='instruction'),
    url(r'^support/$', SupportPage.as_view(), name='support'),
]
