from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from .forms import select_formset, evaluate_formset


class FormsetPage(Page):
    _allow_custom_attributes = True
    formset_class = None

    def get_queryset(self):
        return self.player.items.all()

    def get_context_data(self, bounded_formset=None, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.get_queryset()
        if bounded_formset:
            formset = bounded_formset
        else:
            formset = self.formset_class(instance=self.player, queryset=q)
        context['formset'] = formset
        return context

    def post(self):
        self.object = self.get_object()
        self.form = self.get_form(data=self.request.POST, files=self.request.FILES, instance=self.object)
        q = self.get_queryset()
        formset = self.formset_class(self.request.POST, instance=self.player, queryset=q)
        if not formset.is_valid():
            context = self.get_context_data(bounded_formset=formset, form=self.form)
            return self.render_to_response(context)
        formset.save()
        return super().post()


class Select(FormsetPage):
    formset_class = select_formset


class Evaluate(FormsetPage):
    formset_class = evaluate_formset

    def get_queryset(self):
        return self.player.items.filter(selected=True)


class Results(Page):
    def vars_for_template(self):
        return {'persons': self.player.items.filter(selected=True, evaluation__isnull=False)}


page_sequence = [
    Select,
    Evaluate,
    Results,
]
