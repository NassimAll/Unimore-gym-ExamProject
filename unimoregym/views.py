from django.contrib import messages

from .forms import *
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from braces.views import GroupRequiredMixin
from django.contrib.auth import views as auth_views


# Create your views here.
@login_required
def homeGym(request):
    return render(request, template_name="gym/home_logged.html")

@login_required
def profilePage(request):
    user = request.user
    if request.method == 'POST':
        form = UpdateImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('unimoregym:profile')
    else:
        form = UpdateImageForm(instance=user)

    context = {
        'user': user,
        'form': form
    }
    return render(request, 'gym/user/user_page.html', context)

class PasswordChangeView(auth_views.PasswordChangeView):# UTILIZZO VIEW PREDEFINITE DI DJANGI
    template_name = 'gym/user/change_password.html'
    success_url = reverse_lazy('unimoregym:password_change_done')

class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):# UTILIZZO VIEW PREDEFINITE DI DJANGI
    template_name = 'gym/user/change_password_succces.html'

@login_required
def profile_update(request): #UPDATE DATI UTENTE, SEPRATO DA FOTO PROFILO
    user = request.user
    if request.method == 'POST':
        form = GymUserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('unimoregym:profile')
    else:
        form = GymUserUpdateForm(instance=user)

    return render(request, 'gym/user/user_data_modify.html', {'form': form})

class CorsoListView(ListView): #llista dei corsi con funzioni di ricerca
    titolo = "Corsi offerti"
    model = Corso
    template_name = "gym/data_list/list_corsi.html"
    context_object_name = 'corsi_list'

    def get_queryset(self): #filtriamo a seconda dei campi inseriti nel form
        queryset = Corso.objects.all().order_by('nome')
        nome_query = self.request.GET.get('nome')
        categoria_query = self.request.GET.get('categoria')
        valutazione_query = self.request.GET.get('valutazione_media')

        if nome_query:
            queryset = queryset.filter(nome__icontains=nome_query)
        if categoria_query:
            queryset = queryset.filter(categoria__icontains=categoria_query)
        if valutazione_query:
            queryset = queryset.filter(valutazione_media__gte=valutazione_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CorsoSearchForm(self.request.GET)
        context['titolo'] = self.titolo
        return context

class AbbonamentoListView(ListView): #lista abbonamenti
    titolo = "I nostri piani di abbonamento"
    model = Abbonamento
    template_name = "gym/data_list/list_abbonamenti.html"

class TrainerListView(ListView): #llista allenatori
    titolo = "Il nostro staff"
    model = Trainer
    template_name = "gym/data_list/list_trainers.html"

class AttivazioneAbbonamento(LoginRequiredMixin, DetailView): #dettaglio per prenotare abb
    model = Abbonamento
    template_name = 'gym/detail_abb.html'
    context_object_name = 'abbonamento'

    def post(self, request, *args, **kwargs):
        abb = self.get_object()
        user = request.user

        # Controlla se l'utente ha già un abbonamento attivo
        Abb_attivi = AbbonamentiAttivi.objects.filter(fk_utente=user)
        if Abb_attivi.exists():
            for attivo in Abb_attivi:
                # CONTROLLO CHE NON VOGLIA AVERE DUE ABBONAMENTI PC
                if attivo.fk_abbonamento.codice_abbonamento.startswith("PC") and (abb.codice_abbonamento.startswith("PC") or abb.codice_abbonamento.startswith("PT")):
                    return render(request, 'gym/detail_abb.html', {
                        'abbonamento': abb,
                        'error_message': 'Hai già un pacchetto corsi attivo non puoi attivarne un altro.'
                    })
                # CONTROLLO CHE NON VOGLIA AVERE DUE ABBONAMENTI PP
                if attivo.fk_abbonamento.codice_abbonamento.startswith("PP") and (abb.codice_abbonamento.startswith("PP") or abb.codice_abbonamento.startswith("PT")):
                    return render(request, 'gym/detail_abb.html', {
                        'abbonamento': abb,
                        'error_message': 'Hai già un pacchetto sala pesi attivo non puoi attivarne un altro.'
                    })
                # CONTROLLO CHE NON VOGLIA AVERE UN ALTRO ABBONAMENTO SE HA GIA IL PT
                if attivo.fk_abbonamento.codice_abbonamento.startswith("PT"):
                    if abb.codice_abbonamento.startswith("PC") or abb.codice_abbonamento.startswith("PT") or abb.codice_abbonamento.startswith("PP"):
                        return render(request, 'gym/detail_abb.html', {
                            'abbonamento': abb,
                            'error_message': 'Hai già un pacchetto completo attivo non puoi attivarne un altro differente.'
                        })

        # Genera il QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"{user.username}-{abb.codice_abbonamento}")
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        qr_file = File(buffer, name=f"{user.username}_{abb.codice_abbonamento}.png")

        if abb.codice_abbonamento.startswith("PC"):
            # Crea l'abbonamento attivo PC
            active_abb = AbbonamentiAttivi(
                fk_utente=user,
                fk_abbonamento=abb,
                qr_abbonamento=qr_file,
                utilizzi_rimanenti=abb.durata_massima
            )
        else:
            active_abb = AbbonamentiAttivi(
                fk_utente=user,
                fk_abbonamento=abb,
                qr_abbonamento=qr_file,
            )
        active_abb.save()

        return redirect('unimoregym:success_page')

@login_required #MOSTRA LE SESSIONI DI UN CORSO SOLO
def sessioni_corso(request, corso_id): #VIEW PER LA PRENOTAZIONE DELLA SESSIONE PER UN DETERMINATO CORSO
    corso = get_object_or_404(Corso, pk=corso_id)
    user = request.user

    #FACCIAMO GIA FILTRO MOSTRANDO SOLO LE SESSIONI PRENOTABILI ESCLUDENDO QUELLE GIA PRENOTATE
    prenotate = PrenotazioneUtenteCorso.objects.filter(fk_utente=user).values_list('fk_sessione_id', flat=True)
    today = timezone.now().date()

    sessioni = SessioneCorso.objects.filter(fk_corso=corso, data__gte=today).exclude(idSessione__in=prenotate).order_by('data', 'ora')

    if request.method == 'POST':
        sessione_id = request.POST.get('sessione_id')
        sessione = get_object_or_404(SessioneCorso, pk=sessione_id)

        # Recuperare gli abbonamenti attivi dell'utente
        abbonamenti_attivi = AbbonamentiAttivi.objects.filter(fk_utente=user)

        if not abbonamenti_attivi.exists(): #se non ha abbonamenti
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai un abbonamento attivo. Per favore, acquista un abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)

        # Inizializzare variabili di controllo per i tipi di abbonamento
        pp = False
        pc = False
        pt = False
        pc_utilizzi_rimanenti = 0

        # Verificare i tipi di abbonamenti attivi
        for abbonamento_attivo in abbonamenti_attivi:
            codice_abbonamento = abbonamento_attivo.fk_abbonamento.codice_abbonamento
            if codice_abbonamento.startswith('PP'):
                pp = True
            elif codice_abbonamento.startswith('PC'):
                pc = True
                pc_utilizzi_rimanenti += abbonamento_attivo.utilizzi_rimanenti
            elif codice_abbonamento.startswith('PT'):
                pt = True

        # Logica di prenotazione basata sui tipi di abbonamento
        if pp and not (pc or pt):
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai un abbonamento che ti permette di fare ciò. Per favore, acquista un abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)
        elif pc and pc_utilizzi_rimanenti <= 0 and not pt:
            abbonamento_pc = abbonamenti_attivi.get(fk_abbonamento__codice_abbonamento__startswith='PC')
            abbonamento_pc.delete()
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai un abbonamento che ti permette di fare ciò. Per favore, acquista un abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)
        elif pc and pc_utilizzi_rimanenti > 0:
            abbonamento_pc = abbonamenti_attivi.get(fk_abbonamento__codice_abbonamento__startswith='PC')
            abbonamento_pc.utilizzi_rimanenti -= 1
            abbonamento_pc.save()


        # Controllo se l'utente ha già prenotato un altro corso nella stessa data e ora
        if PrenotazioneUtenteCorso.objects.filter(
                fk_utente=user,
                fk_sessione__data=sessione.data,
                fk_sessione__ora=sessione.ora).exists():
            ctx = {'corso': corso, 'sessioni': sessioni, 'error_message': 'Hai già prenotato un altro corso nella stessa data e ora.'}
            return render(request, 'gym/detail_corso.html', ctx)

        #Controllo che il corso sia disponibile
        if sessione.disponibilita > 0:
            PrenotazioneUtenteCorso.objects.create(
                fk_utente=user,
                fk_sessione=sessione
            )
            sessione.disponibilita -= 1
            sessione.save()
            return redirect('unimoregym:mieprenotazioni')
        else:
            # caso in cui non ci siano più disponibilità
            ctx = {'corso': corso, 'sessioni': sessioni, 'error_message': 'Non ci sono più posti disponibili per questa sessione.'}
            return render(request, 'gym/detail_corso.html', ctx)

    ctx = {'corso': corso, 'sessioni': sessioni}
    return render(request, 'gym/detail_corso.html', ctx)

@login_required
def sessioni_disponibili(request): #MOSTRA UNA LISTA DI TUTTE LE SESSIONI
    #Recupero le sessioni che ha gia e le sottraggo dalle disponibili cosi da evitare che voglia prenotare di nuovo la stessa
    today = timezone.now().date()
    user = request.user

    prenotate = PrenotazioneUtenteCorso.objects.filter(fk_utente=user).values_list('fk_sessione_id', flat=True)
    sessioni = SessioneCorso.objects.exclude(idSessione__in=prenotate, data__gte=today).order_by('data', 'ora')

    if request.method == 'POST':
        sessione_id = request.POST.get('sessione_id')
        sessione = get_object_or_404(SessioneCorso, pk=sessione_id)

        # Recuperare gli abbonamenti attivi dell'utente
        abbonamenti_attivi = AbbonamentiAttivi.objects.filter(fk_utente=user)

        if not abbonamenti_attivi.exists():
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai un abbonamento attivo. Per favore, acquista un abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)

        # Inizializzare variabili di controllo per i tipi di abbonamento
        pp = False
        pc = False
        pc_utilizzi_rimanenti = 0

        # Verificare i tipi di abbonamenti attivi
        for abbonamento_attivo in abbonamenti_attivi:
            codice_abbonamento = abbonamento_attivo.fk_abbonamento.codice_abbonamento
            print(codice_abbonamento)
            if codice_abbonamento.startswith('PP'):
                pp = True
            elif codice_abbonamento.startswith('PC'):
                pc = True
                pc_utilizzi_rimanenti += abbonamento_attivo.utilizzi_rimanenti

            print(pc)
            print(pp)

        # Logica di prenotazione basata sui tipi di abbonamento
        if pp and not pc :
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai un abbonamento che ti permette di fare ciò. Per favore, acquista un abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)
        elif pc and pc_utilizzi_rimanenti == 0:
            abbonamento_pc = abbonamenti_attivi.get(fk_abbonamento__codice_abbonamento__startswith='PC')
            abbonamento_pc.delete()
            ctx = {
                'sessioni': sessioni,
                'error_message': 'Non hai più utilizzi. Per favore, acquista un nuovo abbonamento.',
                'reindirizza': 1
            }
            return render(request, 'gym/sessioni_disponibili.html', ctx)
        elif pc and pc_utilizzi_rimanenti > 0:
            abbonamento_pc = abbonamenti_attivi.get(fk_abbonamento__codice_abbonamento__startswith='PC')
            abbonamento_pc.utilizzi_rimanenti -= 1
            abbonamento_pc.save()

        # Controllo se l'utente ha già prenotato un altro corso nella stessa data e ora
        if PrenotazioneUtenteCorso.objects.filter(
                fk_utente=user,
                fk_sessione__data=sessione.data,
                fk_sessione__ora=sessione.ora).exists():
            ctx = {'sessioni': sessioni,
                'error_message': 'Hai già prenotato un altro corso nella stessa data e ora.'}
            return render(request, 'gym/sessioni_disponibili.html', ctx)

        # Controllare la disponibilità
        if sessione.disponibilita > 0:
            PrenotazioneUtenteCorso.objects.create(
                fk_utente=user,
                fk_sessione=sessione
            )
            sessione.disponibilita -= 1
            sessione.save()
            return redirect('unimoregym:mieprenotazioni')
        else:
            ctx = {'sessioni': sessioni,
                   'error_message': 'Non ci sono più posti disponibili per questa sessione.'}
            return render(request, 'gym/sessioni_disponibili.html', ctx)

    return render(request, 'gym/sessioni_disponibili.html', {'sessioni': sessioni})


@login_required
def abbonamenti_attivi_utente(request): #MOSTRA LA LISTA DEGLI ABBONAMENTI ATTIVI DI UN UTENTE E PERMETTE DI CANCELLARLI
    #abbonamenti attivi dell'utente
    user = request.user
    abbonamenti_attivi = AbbonamentiAttivi.objects.filter(fk_utente=user)

    #Cancellazzione abbonamento utente
    if request.method == 'POST':
        abbonamento_id = request.POST.get('abbonamento_id')
        abbonamento = get_object_or_404(AbbonamentiAttivi, pk=abbonamento_id, fk_utente=user)

        abbonamento.delete()

        return redirect('unimoregym:myabbonamenti')

    ctx = {'abbonamenti_attivi': abbonamenti_attivi}

    return render(request, 'gym/user/user_abbonamenti_attivi.html', ctx)

@login_required
def user_booking(request):  #MOSTRA TUTTE LE PRENOTAZIONI DI UN SINGOLO UTENTE E GLI PERMETTE DI CANCELLARLE
    #otteniamo l'utente
    user = request.user
    today = timezone.localtime().date()
    print(today)
    # Ottieni le prenotazioni attive per l'utente loggato
    prenotazioni_attive = PrenotazioneUtenteCorso.objects.filter(fk_utente=user, fk_sessione__data__gte=today).order_by('fk_sessione__data', 'fk_sessione__ora')


    if request.method == 'POST':    #PER IL FORM DI CANCELLAZIONE DELLA PRENOTAZIONE
        prenotazione_id = request.POST.get('prenotazione_id')
        prenotazione = get_object_or_404(PrenotazioneUtenteCorso, pk=prenotazione_id, fk_utente=user)

        # Incrementare la disponibilità della sessione
        sessione = prenotazione.fk_sessione
        sessione.disponibilita += 1
        sessione.save()

        # Gestire l'abbonamento se necessario e ridare l'utilizzo all'utente
        abbonamento_pc = AbbonamentiAttivi.objects.filter(fk_utente=user,fk_abbonamento__codice_abbonamento__startswith='PC').first()
        if abbonamento_pc:
            #print(abbonamento_pc)
            abbonamento_pc.utilizzi_rimanenti += 1
            abbonamento_pc.save()

        prenotazione.delete()
        return redirect('unimoregym:mieprenotazioni')

    ctx = {"prenotazioni": prenotazioni_attive}

    return render(request, 'gym/user/user_prenotazioni.html', ctx)

def success_page(request):
    return render(request, 'gym/success.html')

@login_required
def prenota_sessione(request):  #ACTION PER LA PRENOTAZONE, LO USO NELLA RICERCA PER FORNIRE UN ACTION DA ESEGUIRE PER PRENOTARE
    # otteniamo l'utente
    user = request.user
    sessione_id = request.POST.get('sessione_id')
    sessione = get_object_or_404(SessioneCorso, pk=sessione_id)

    # Recuperare gli abbonamenti attivi dell'utente
    abbonamenti_attivi = AbbonamentiAttivi.objects.filter(fk_utente=user)

    if not abbonamenti_attivi.exists():
        form = CercaSessioniForm()
        ctx = {'form': form, 'sessioni': [],
               'error_message': 'Non possiedi abbonamenti per la prenotazione'}
        return render(request, 'gym/ricerca_sessioni.html', ctx)

    # Inizializzare variabili di controllo per i tipi di abbonamento
    pp = False
    pc = False
    pc_utilizzi_rimanenti = 0

    # Verificare i tipi di abbonamenti attivi
    for abbonamento_attivo in abbonamenti_attivi:
        codice_abbonamento = abbonamento_attivo.fk_abbonamento.codice_abbonamento
        print(codice_abbonamento)
        if codice_abbonamento.startswith('PP'):
            pp = True
        elif codice_abbonamento.startswith('PC'):
            pc = True
            pc_utilizzi_rimanenti += abbonamento_attivo.utilizzi_rimanenti

        print(pc)
        print(pp)

    # Logica di prenotazione basata sui tipi di abbonamento
    if pp and not pc:
        form = CercaSessioniForm()
        ctx = {'form': form, 'sessioni': [],
               'error_message': 'Il tuo abbonamento non permette di prenotare corsi.'}
        return render(request, 'gym/ricerca_sessioni.html', ctx)
    elif pc and pc_utilizzi_rimanenti == 0:
        form = CercaSessioniForm()
        ctx = {'form': form, 'sessioni': [],
               'error_message': 'Non hai abbastanza utilizzi rimanenti per prenotare questo corso.'}
        return render(request, 'gym/ricerca_sessioni.html', ctx)
    elif pc and pc_utilizzi_rimanenti > 0:
        abbonamento_pc = abbonamenti_attivi.get(fk_abbonamento__codice_abbonamento__startswith='PC')
        abbonamento_pc.utilizzi_rimanenti -= 1
        abbonamento_pc.save()

    # Controllo se l'utente ha già prenotato un altro corso nella stessa data e ora
    if PrenotazioneUtenteCorso.objects.filter(fk_utente=user,
            fk_sessione__data=sessione.data,
            fk_sessione__ora=sessione.ora).exists():
        form = CercaSessioniForm()
        ctx = {'form': form, 'sessioni': [],
               'error_message': 'Hai già prenotato un altro corso nella stessa data e ora.'}
        return render(request, 'gym/ricerca_sessioni.html', ctx)

    # Controllare la disponibilità
    if sessione.disponibilita > 0:
        PrenotazioneUtenteCorso.objects.create(
            fk_utente=user,
            fk_sessione=sessione
        )
        sessione.disponibilita -= 1
        sessione.save()
        return redirect('unimoregym:mieprenotazioni')
    else:
        form = CercaSessioniForm()
        ctx = {'form': form, 'sessioni': [],
               'error_message': 'Non ci sono più posti disponibili per questa sessione.'}
        return render(request, 'gym/ricerca_sessioni.html', ctx)


@login_required
def ricerca_sessioni(request):
    #View per la ricerca, mostra le sessioni cercate con una serie di filtri, poi per prenotare sono inseriti form per sessione e ogni form usa come action il metodo prenota_sessione
    form = CercaSessioniForm(request.GET or None)
    today = timezone.now().date()
    #PRIMA PRENDO LE PRENOTATE, POI TOLGO LE PRENOTATE DAL TOTALE E INFINE FILTRO IN BASE AI PARAMNETRI CHE MI SONO STATI PASSATI
    prenotate = PrenotazioneUtenteCorso.objects.filter(fk_utente=request.user).values_list('fk_sessione_id', flat=True)
    sessioni = SessioneCorso.objects.exclude(idSessione__in=prenotate, data__gte=today).order_by('data', 'ora')


    if form.is_valid():
        nome_corso = form.cleaned_data.get('nome_corso')
        data_inizio = form.cleaned_data.get('data_inizio')
        data_fine = form.cleaned_data.get('data_fine')
        ora_inizio = form.cleaned_data.get('ora_inizio')
        durata = form.cleaned_data.get('durata')
        categoria = form.cleaned_data.get('categoria')

        if data_inizio:
            sessioni = sessioni.filter(data__gte=data_inizio)
        if data_fine:
            sessioni = sessioni.filter(data__lte=data_fine)
        if ora_inizio:
            sessioni = sessioni.filter(ora__gte=ora_inizio)
        if durata:
            corsi_con_durata = Corso.objects.filter(durata__lte=durata).values_list('idcorso', flat=True)
            sessioni = sessioni.filter(fk_corso_id__in=corsi_con_durata)
        if categoria:
            sessioni = sessioni.filter(fk_corso__categoria__icontains=categoria)
        if nome_corso:
            sessioni = sessioni.filter(fk_corso__nome__icontains=nome_corso)

        return render(request, 'gym/ricerca_sessioni.html', {'form': form, 'sessioni': sessioni})

    return render(request, 'gym/ricerca_sessioni.html', {'form': form, 'sessioni': []})


@login_required
def rate_corso(request, corso_id): #VIEW PER LA VALUTAZIONE DI UN CORSO
    corso = get_object_or_404(Corso, idcorso=corso_id)
    exist_rating = Rating.objects.filter(corso=corso, user=request.user).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if exist_rating: #se esiste gia cancello e poi ricreo
                exist_rating.delete()
                rating = form.save(commit=False)
                rating.corso = corso
                rating.user = request.user
                rating.save()
            else:
                rating = form.save(commit=False)
                rating.corso = corso
                rating.user = request.user
                rating.save()

            # Calcolo la valutazione media
            total_rating = sum(r.stelle for r in corso.ratings.all())
            corso.valutazione_media = total_rating / corso.ratings.count()
            corso.save()
            return redirect('unimoregym:ListaCorsi')
    else:
        form = RatingForm(instance=exist_rating) #ricarico la recensione gia esistente
    return render(request, 'gym/rating_corso.html', {'form': form, 'corso': corso})

@login_required
def list_ratings_corso(request, corso_id): #VIEW PER LA stampa della lista delle recensioni
    corso = get_object_or_404(Corso, idcorso=corso_id)
    recensioni = Rating.objects.filter(corso=corso)

    ctx = {'corso': corso , 'recensioni': recensioni}
    return render(request, 'gym/data_list/list_rating_corso.html', ctx)


# --------------------------------------------------------------------------
#Views per le funzionalità dell'owner
class SituazionePrenotazioniListView(GroupRequiredMixin, ListView):
    group_required = ["Owner"]
    titolo = "Lista delle prenotazioni"
    empty_message = "Non ci sono prenotazioni"
    model = PrenotazioneUtenteCorso
    template_name = "gym/gestore_views/resoconto_prenotazioni.html"


class SituazioneAbbonamentiAttiviListView(GroupRequiredMixin, ListView):
    group_required = ["Owner"]
    titolo = "Lista degli abbonamenti registrati"
    empty_message = "Non ci sono abbonamenti registrati"
    model = AbbonamentiAttivi
    template_name = "gym/gestore_views/resoconto_AbbAttivi.html"

class CreateDefaultView(GroupRequiredMixin, CreateView):
    group_required = ["Owner"]
    title = "Crea un Corso"
    form_class = CreateCorsoForm
    template_name = "gym/gestore_views/create_obj.html"
    success_url = reverse_lazy("unimoregym:homeGym")

class CreateTrainerView(CreateDefaultView):
    title = "Aggiungi un Trainer allo staff"
    form_class = CreateTrainerForm

class CreateAbbonamentoView(CreateDefaultView):
    title = "Aggiungi un nuovo Abbonamento"
    form_class = CreateAbbonamentoForm

class CreateSessioneView(CreateDefaultView):
    title = "Aggiungi una nuova sessione"
    form_class = CreateSessioneForm

class CorsoDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Owner"]
    model = Corso
    success_url = reverse_lazy('unimoregym:ListaCorsi')

class AbbonamentoDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Owner"]
    model = Abbonamento
    success_url = reverse_lazy('unimoregym:ListaAbbonamenti')

class TrainerDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Owner"]
    model = Trainer
    success_url = reverse_lazy('unimoregym:ListaStaff')

class SessioneDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Owner"]
    model = SessioneCorso
    success_url = reverse_lazy('unimoregym:sessioni_disponibili')

class AbbonamentoUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Owner"]
    model = Abbonamento
    title = "Aggiorna Abbonamento"
    form_class = UpdateAbbonamentoForm
    template_name = 'gym/gestore_views/update_entry.html'
    success_url = reverse_lazy('unimoregym:ListaAbbonamenti')

class SessioneUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Owner"]
    model = SessioneCorso
    form_class = CreateSessioneForm
    title = "Aggiorna Sessione"
    template_name = 'gym/gestore_views/update_entry.html'
    success_url = reverse_lazy('unimoregym:sessioni_disponibili')

class CorsoUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Owner"]
    model = Corso
    form_class = CreateCorsoForm
    title = "Aggiorna Corso"
    template_name = 'gym/gestore_views/update_entry.html'
    success_url = reverse_lazy('unimoregym:ListaCorsi')
