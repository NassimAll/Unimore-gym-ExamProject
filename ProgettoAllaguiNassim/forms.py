from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from unimoregym.models import GymUser
from django.contrib.auth.models import Group

class SignUpClientForm(UserCreationForm):
    class Meta:
        model = GymUser
        fields = ('username', 'email', 'nome', 'cognome', 'codice_fiscale', 'data_nascita')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email: test@test.com'}),
            'data_nascita': forms.DateInput(attrs={'type': 'date'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            g = Group.objects.get(name='Client')
            g.user_set.add(user)
        return user

    def clean_codice_fiscale(self):
        codice_fiscale = self.cleaned_data.get('codice_fiscale')
        if len(codice_fiscale) != 16:
            raise forms.ValidationError('Il codice fiscale deve essere di 16 caratteri.')
        return codice_fiscale


class SignUpOwnerForm(UserCreationForm):
    class Meta:
        model = GymUser
        fields = ('username', 'nome', 'cognome', 'codice_fiscale')
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email: test@test.com'}),
            'data_nascita': forms.DateInput(attrs={'type': 'date'})
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            g = Group.objects.get(name="Owner")
            g.user_set.add(user)
        return user

    def clean_codice_fiscale(self):
        codice_fiscale = self.cleaned_data.get('codice_fiscale')
        if len(codice_fiscale) != 16:
            raise forms.ValidationError('Il codice fiscale deve essere di 16 caratteri.')
        return codice_fiscale

    def clean_data_nascita(self):
        data_nascita = self.cleaned_data.get('data_nascita')
        today = date.today()
        age = today.year - data_nascita.year - ((today.month, today.day) < (data_nascita.month, data_nascita.day))
        if age < 15:
            raise forms.ValidationError('Devi avere almeno 15 anni.')
        return data_nascita