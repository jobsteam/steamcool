from django import forms

from games.models import Game


class CheckboxWidget(forms.CheckboxSelectMultiple):
    template_name = 'form/checkbox.html'


class FilterForm(forms.ModelForm):
    """
    Форма для фильтрации игр по параметрам.
    """
    price_min = forms.IntegerField(
        label='Цена от',
        required=False)
    price_max = forms.IntegerField(
        label='Цена до',
        required=False)

    class Meta:
        fields = ['price_min', 'price_max', 'genre', 'store_activation',
                  'mode']
        model = Game
        widgets = {
            'genre': CheckboxWidget,
            'store_activation': CheckboxWidget,
            'mode': CheckboxWidget,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        store_field = self.fields['store_activation']
        store_field.choices = store_field.choices[1:]
