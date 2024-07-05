from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from .models import *
class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = GymUser
        fields = ['profile_image']

    def __init__(self, *args, **kwargs):
        super(UpdateImageForm, self).__init__(*args, **kwargs)
        self.fields['profile_image'].label = 'Carica foto'


class GymUserUpdateForm(forms.ModelForm):
    class Meta:
        model = GymUser
        fields = ['email', 'data_nascita']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'test@test.com'}),
            'data_nascita': forms.DateInput(attrs={'type': 'date'}, ),
        }

    def __init__(self, *args, **kwargs):
        super(GymUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['data_nascita'].required = True

    def clean_data_nascita(self):
        data_nascita = self.cleaned_data.get('data_nascita')
        today = date.today()
        age = today.year - data_nascita.year - ((today.month, today.day) < (data_nascita.month, data_nascita.day))
        if age < 15:
            raise ValidationError('Devi avere almeno 15 anni.')
        return data_nascita

class UpdateAbbonamentoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "UpdateAbbonamento_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Aggiorna Abbonamento"))

    class Meta:
        model = Abbonamento
        fields = ['nome', 'tariffa', 'durata_massima']

class CorsoSearchForm(forms.Form): #FORM PER RICERCA CORSI
    nome = forms.CharField(required=False, label='Nome')
    categoria = forms.CharField(required=False, label='Categoria')
    valutazione_media = forms.FloatField(required=False, label='Valutazione Media Minima')

    def __init__(self, *args, **kwargs):
        super(CorsoSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('search', 'Cerca'))

class CercaSessioniForm(forms.Form):
    nome_corso = forms.CharField(required=False, max_length=255)
    data_inizio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fine = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    ora_inizio = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time'}))
    durata = forms.IntegerField(required=False, help_text="Durata in minuti")
    categoria = forms.CharField(required=False, max_length=255)

    def __init__(self, *args, **kwargs):
        super(CercaSessioniForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.add_input(Submit('search', 'Cerca'))

class CreateAbbonamentoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addAbbonamento_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Abbonamento"))

    class Meta:
        model = Abbonamento
        fields = ['codice_abbonamento', 'nome', 'tariffa', 'durata_massima', 'descrizione']

class CreateTrainerForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addTrainer_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Trainer"))

    class Meta:
        model = Trainer
        fields = ['nome','cognome','descrizione']

class CreateCorsoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addCorso_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Corso"))

    class Meta:
        model = Corso
        fields = ['idcorso','nome', 'categoria','descrizione','fk_trainer']

class UpdateSessioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "UpdateSessione_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiorna Sessione"))

    SALA_CHOICES = [(i, f"Sala {i}") for i in range(1, 11)]

    sala_corso = forms.ChoiceField(choices=SALA_CHOICES, label="Sala Corso")

    class Meta:
        model = SessioneCorso
        fields = ['fk_corso','data','ora','sala_corso', 'disponibilita']
        widgets = {
            'ora': forms.TimeInput(attrs={'placeholder': 'Format: HH:MM'}),
            'data': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        fk_corso = cleaned_data.get('fk_corso')
        data = cleaned_data.get('data')
        ora = cleaned_data.get('ora')
        sala_corso = cleaned_data.get('sala_corso')

        # Check if another course is scheduled in the same room, date, and time
        same_room_session = SessioneCorso.objects.filter(
            data=data,
            ora=ora,
            sala_corso=sala_corso
        ).exclude(fk_corso=fk_corso).exists()

        if same_room_session:
            raise ValidationError("Un altro corso è già programmato in questa sala, data e ora.")


class CreateSessioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addSessione_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Aggiungi Sessione"))

    SALA_CHOICES = [(i, f"Sala {i}") for i in range(1, 11)]

    sala_corso = forms.ChoiceField(choices=SALA_CHOICES, label="Sala Corso")

    class Meta:
        model = SessioneCorso
        fields = ['fk_corso','data','ora','sala_corso', 'disponibilita']
        widgets = {
            'ora': forms.TimeInput(attrs={'placeholder': 'Format: HH:MM'}),
            'data': forms.DateInput(attrs={'type': 'date'})
        }

    def clean(self):
        cleaned_data = super().clean()
        fk_corso = cleaned_data.get('fk_corso')
        data = cleaned_data.get('data')
        ora = cleaned_data.get('ora')
        sala_corso = cleaned_data.get('sala_corso')

        # Controllo se inserisce una sessione identica
        if fk_corso and data and ora and sala_corso:
            existing_session = SessioneCorso.objects.filter(
                fk_corso=fk_corso,
                data=data,
                ora=ora,
                sala_corso=sala_corso
            ).exists()

            if existing_session:
                raise ValidationError("Una sessione con questo corso, data, ora e aula esiste già.")

            # Check if another course is scheduled in the same room, date, and time
            same_room_session = SessioneCorso.objects.filter(
                data=data,
                ora=ora,
                sala_corso=sala_corso
            ).exclude(fk_corso=fk_corso).exists()

            if same_room_session:
                raise ValidationError("Un altro corso è già programmato in questa sala, data e ora.")

            # Check if the same course is scheduled in a different room, date, and time
            same_course_different_room = SessioneCorso.objects.filter(
                fk_corso=fk_corso,
                data=data,
                ora=ora
            ).exclude(sala_corso=sala_corso).exists()

            if same_course_different_room:
                raise ValidationError("Questo corso è già programmato in un'altra sala alla stessa data e ora.")

            # Check if the same course is scheduled on the same date but different time and room
            same_course_same_day_different_time_room = SessioneCorso.objects.filter(
                fk_corso=fk_corso,
                data=data
            ).exclude(ora=ora, sala_corso=sala_corso).exists()

            if same_course_same_day_different_time_room:
                raise ValidationError("Questo corso è già programmato in un'altra sala o ora alla stessa data.")

        return cleaned_data

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stelle', 'commento']
        widgets = {
            'stelle': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        }