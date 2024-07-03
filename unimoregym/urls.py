
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "unimoregym"

urlpatterns = [
    path("homeUser/", homeGym, name="homeGym"),
    path("profile/", profilePage, name="profile"),
    path('profile/update', profile_update, name='update_profile'),
    path('profile/password/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path("corsi/", CorsoListView.as_view(), name="ListaCorsi"),
    path("abbonamenti/", AbbonamentoListView.as_view(), name="ListaAbbonamenti"),
    path("trainers/", TrainerListView.as_view(), name="ListaStaff"),
    path('iscrizioneAbbonamento/<str:pk>/', AttivazioneAbbonamento.as_view(), name='iscrizione_abb'),
    path('success/', success_page, name='success_page'),
    path('mieprenotazioni/', user_booking, name='mieprenotazioni'),
    path('create_abbonamento/', CreateAbbonamentoView.as_view(), name='create_abbonamento'),
    path('create_trainer/', CreateTrainerView.as_view(), name='create_trainer'),
    path('create_corso', CreateDefaultView.as_view(), name='create_corso'),
    path('create_sessione', CreateSessioneView.as_view(), name='create_sessione'),
    path('corsi/delete/<pk>/', CorsoDeleteView.as_view(), name='corso_delete'),
    path('abbonamenti/delete/<pk>/', AbbonamentoDeleteView.as_view(), name='abb_delete'),
    path('trainer/delete/<pk>/', TrainerDeleteView.as_view(), name='trainer_delete'),
    path('sessione/delete/<pk>/', SessioneDeleteView.as_view(), name='sessione_delete'),
    path('situazione_abbonamenti/', SituazioneAbbonamentiAttiviListView.as_view(), name='situazione_abbonamenti'),
    path('situazione_prenotazioni/', SituazionePrenotazioniListView.as_view(), name='situazione_prenotazioni'),
    path('corso/<str:corso_id>/sessioni/', sessioni_corso, name='sessioni_corso'),
    path('sessioni/disponibili/', sessioni_disponibili, name='sessioni_disponibili'),
    path('myabbonamenti/', abbonamenti_attivi_utente, name='myabbonamenti'),
    path('cerca_sessioni/', ricerca_sessioni, name='cerca_sessioni'),
    path('prenota_sessioni/', prenota_sessione, name='prenota_sessione'),
    path('corso/<str:corso_id>/rate/', rate_corso, name='rate_corso'),
    path('corso/<str:corso_id>/ratings', list_ratings_corso, name='list_ratings_corso')

]
