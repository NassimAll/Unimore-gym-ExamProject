import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class Abbonamento(models.Model):
    codice_abbonamento = models.CharField(max_length=255, primary_key=True)
    nome = models.CharField(max_length=255)
    tariffa = models.DecimalField(max_digits=10, decimal_places=2)
    durata_massima = models.IntegerField()
    descrizione = models.TextField()

    class Meta:
        verbose_name_plural = "Abbonamenti"


class Trainer(models.Model):
    nome = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    descrizione = models.TextField()

    def __str__(self):
        out = self.nome + " " + self.cognome + ". "
        return out

    class Meta:
        verbose_name_plural = "Trainers"

class Corso(models.Model):
    idcorso = models.CharField(max_length=255, primary_key=True)
    nome = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, default="")
    descrizione = models.TextField()
    durata = models.IntegerField(default=60, help_text="Durata in minuti")
    fk_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
    valutazione_media = models.FloatField(default=0)

    def __str__(self):
        out =  self.nome + ".\n"
        return out

    class Meta:
        verbose_name_plural = "Corsi"

class SessioneCorso(models.Model):
    idSessione = models.AutoField(primary_key=True)
    ora = models.TimeField()
    data = models.DateField()
    sala_corso = models.IntegerField()
    disponibilita = models.IntegerField(default=30)
    fk_corso = models.ForeignKey(Corso, on_delete=models.CASCADE)

    def __str__(self):
        out =  "Corso: " + self.fk_corso.nome + "; In sala: N^" + str(self.sala_corso) + "; Data: " + self.data.__str__() + " alle " + self.ora.__str__()
        return out

class GymUser(AbstractUser):
    nome = models.CharField(max_length=255, default='')
    cognome = models.CharField(max_length=255, default='')
    codice_fiscale = models.CharField(max_length=16, default='')
    data_nascita = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='default/default_user.png')

    objects = CustomUserManager()

    def __str__(self):
        out =  self.username
        return out

class PrenotazioneUtenteCorso(models.Model):
    idPrenotazione = models.AutoField(primary_key=True)
    fk_utente = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    fk_sessione = models.ForeignKey(SessioneCorso, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField(auto_now_add=True)

class AbbonamentiAttivi(models.Model):
    idabbonamento = models.AutoField(primary_key=True)
    fk_utente = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    fk_abbonamento = models.ForeignKey(Abbonamento, on_delete=models.CASCADE)
    data_prenotazione = models.DateField(auto_now_add=True)
    data_scadenza = models.DateField(null=True, blank=True)
    utilizzi_rimanenti = models.IntegerField(null=True, blank=True)
    qr_abbonamento = models.ImageField(upload_to='abbonamenti/', default='default/default_qr.jpg')

    def save(self, *args, **kwargs):
        if not self.data_scadenza and not self.fk_abbonamento.codice_abbonamento.startswith("PC"):
            self.data_scadenza = datetime.date.today() + timedelta(days=self.fk_abbonamento.durata_massima)
            print(self.data_scadenza)
        super().save(*args, **kwargs)

class Rating(models.Model):
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(GymUser, on_delete=models.CASCADE)
    stelle = models.IntegerField()
    commento = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('corso', 'user')