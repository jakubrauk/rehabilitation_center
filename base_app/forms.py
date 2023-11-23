from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from base_app.models import Visit, Patient, Rehabilitator
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    # either rehabilitator or patient (default)
    register_as = forms.CharField(
        widget=forms.HiddenInput(),
        initial='patient'
    )

    error_messages = {
        "password_mismatch": _("Podane hasła różnią się od siebie."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['username'].help_text = "Wymagane. Conajmniej 150 znaków. Dozwolone znaki to litery, cyfry oraz @/./+/-/_."
        self.fields['password1'].label = 'Hasło'
        self.fields['password1'].help_text = ("<ul>"
                                             "<li>Hasło nie może być zbyt podobne do nazwy użytkownika.</li>"
                                              "<li>Hasło musi składać się z conajmniej 8 znaków.</li>"
                                              "<li>Twoje hało nie może być często używanym hasłem.</li>"
                                              "<li>Twoje hasło nie może składać się wyłącznie z cyfr.</li>"
                                             "</ul>")
        self.fields['password2'].label = 'Potwierdź hasło'
        self.fields['password2'].help_text = "Wprowadź to samo hasło w celu weryfikacji."

    def save(self, *args, **kwargs):
        user = super().save(commit=True)
        register_as = self.cleaned_data.get('register_as')
        if register_as == 'patient':
            patient = Patient.objects.create(user=user)
        elif register_as == 'rehabilitator':
            rehabilitator = Rehabilitator.objects.create(user=user)

        return user


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Wprowadź poprawną nazwę użytkownika oraz hasło. Pamiętaj, że oba pola są case-sensitive."
        ),
        "inactive": _("To konto jest nieaktywne"),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['password'].label = 'Hasło'
        self.fields['username'].label = 'Nazwa użytkownika'


class VisitForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Data rozpoczęcia wizyty'
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Data zakończenia wizyty'
    )

    class Meta:
        model = Visit
        fields = ('start_date', 'end_date', 'description', 'rehabilitator')

        labels = {
            'start_date': 'Data rozpoczęcia wizyty',
            'end_date': 'Data zakończenia wizyty',
            'description': 'Opis',
        }

        widgets = {
            'rehabilitator': forms.HiddenInput()
        }

