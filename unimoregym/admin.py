from django.contrib import admin

from unimoregym.models import *

admin.site.register(Corso)
admin.site.register(Abbonamento)
admin.site.register(Trainer)
admin.site.register(SessioneCorso)
admin.site.register(GymUser)
admin.site.register(PrenotazioneUtenteCorso)
admin.site.register(AbbonamentiAttivi)


# Register your models here.
