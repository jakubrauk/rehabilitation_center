from django import forms

from base_app.models import Visit


class VisitForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d-%m-%Y %H:%M'),
        input_formats=['%d-%m-%Y %H:%M']
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(format='%d-%m-%Y %H:%M'),
        input_formats=['%d-%m-%Y %H:%M']
    )

    class Meta:
        model = Visit
        fields = '__all__'

