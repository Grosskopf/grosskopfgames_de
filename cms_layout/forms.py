from cms.models import CMSPlugin
from django import forms


class UpdateCSSForm(forms.ModelForm):
    css__key = forms.CharField()
    css__value = forms.CharField()

    class Meta:
        model = CMSPlugin
        fields = [
            'css__key',
            'css__value',
        ]
