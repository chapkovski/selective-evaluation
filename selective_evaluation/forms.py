from .models import Item, Player, Constants
from django.forms import inlineformset_factory, BaseInlineFormSet, ValidationError
from django.forms import ModelForm, BooleanField, RadioSelect
from otree.api import widgets


class SelectForm(ModelForm):
    class Meta:
        model = Item
        fields = ['selected']
        widgets = {
            'selected': widgets.RadioSelectHorizontal,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected'].widget.choices = ((True, 'Yes'), (False, 'No'))
        self.fields['selected'].widget.attrs['required'] = 'required'


class EvaluateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['evaluation']
        widgets = {
            'evaluation': widgets.RadioSelectHorizontal,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evaluation'].widget.choices = [(i, i) for i in range(10)]
        self.fields['evaluation'].widget.attrs['required'] = 'required'


select_formset = inlineformset_factory(Player, Item, can_delete=False, extra=0, form=SelectForm, )
evaluate_formset = inlineformset_factory(Player, Item, can_delete=False, extra=0, form=EvaluateForm, )
