from django.urls import path
from .views import *

urlpatterns = [
    path('prenotazioni/', prenotazioni_corsi_utente, name='api-prenotazioni-corsi'),
    path('abbonamenti/', abbonamenti_attivi_utente, name='api-abbonamenti-attivi'),
    path('recommended-corsi/', recommended_corsi_api, name='api-recommended-corsi'),

]
