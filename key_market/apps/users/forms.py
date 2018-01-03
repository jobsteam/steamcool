from django import forms

from users.models import User


class MailForm(forms.ModelForm):
    payment = forms.CharField(
        label='способ оплаты',
        required=True)

    class Meta:
        model = User
        fields = '__all__'
