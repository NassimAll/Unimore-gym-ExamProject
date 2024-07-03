from .models import Corso, SessioneCorso, Abbonamento, AbbonamentiAttivi, GymUser, PrenotazioneUtenteCorso
from .forms import CreateSessioneForm
from django.test import TestCase, Client
from django.urls import reverse
from io import BytesIO
import qrcode
from django.core.files import File
from django.utils import timezone

#TEST PER L'ATTIVAZIONE DEI VARI ABBINAMENTI CONSIDERANDO LE COMBINAZIONI
class AttivazioneAbbonamentoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = GymUser.objects.create_user(
            username='testuser',email='test@test.it', password='12345', nome='Test', cognome='User', codice_fiscale='ABCDEF12G34H567I'
        )
        self.client.login(username='testuser', password='12345')

        # Creare abbonamenti
        self.abbonamento_pc = Abbonamento.objects.create(
            codice_abbonamento='PC001', nome='Pacchetto Corsi', tariffa=100.00, durata_massima=30,
            descrizione='Pacchetto corsi'
        )
        self.abbonamento_pp = Abbonamento.objects.create(
            codice_abbonamento='PP001', nome='Pacchetto Palestra', tariffa=80.00, durata_massima=30,
            descrizione='Pacchetto palestra'
        )
        self.abbonamento_pt = Abbonamento.objects.create(
            codice_abbonamento='PT001', nome='Pacchetto Totale', tariffa=150.00, durata_massima=30,
            descrizione='Pacchetto totale'
        )

    def test_attivazione_abbonamento_senza_abbonamenti_attivi(self):
        response = self.client.post(reverse('unimoregym:iscrizione_abb', args=[self.abbonamento_pc.codice_abbonamento]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('unimoregym:success_page'))
        self.assertTrue(
            AbbonamentiAttivi.objects.filter(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc).exists())

    def test_attivazione_abbonamento_con_abbonamento_pc_attivo(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc)
        response = self.client.post(reverse('unimoregym:iscrizione_abb', args=[self.abbonamento_pc.codice_abbonamento]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hai già un pacchetto corsi attivo non puoi attivarne un altro.')

    def test_attivazione_abbonamento_con_abbonamento_pp_attivo(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pp)
        response = self.client.post(reverse('unimoregym:iscrizione_abb', args=[self.abbonamento_pp.codice_abbonamento]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hai già un pacchetto sala pesi attivo non puoi attivarne un altro.')

    def test_attivazione_abbonamento_con_abbonamento_pt_attivo(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pt)
        response = self.client.post(reverse('unimoregym:iscrizione_abb', args=[self.abbonamento_pc.codice_abbonamento]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hai già un pacchetto completo attivo non puoi attivarne un altro differente.')

    def test_generazione_qr_code(self):
        response = self.client.post(reverse('unimoregym:iscrizione_abb', args=[self.abbonamento_pc.codice_abbonamento]))
        self.assertEqual(response.status_code, 302)
        active_subscription = AbbonamentiAttivi.objects.get(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc)
        self.assertIsNotNone(active_subscription.qr_abbonamento)

        # Controllare il contenuto del QR code
        buffer = BytesIO(active_subscription.qr_abbonamento.read())
        img = qrcode.make(buffer.getvalue())
        self.assertIsNotNone(img)

# TEST INSERIMENTO DELLE SESSIONI DA PARTE DELL'OWNER
class SessioneCorsoFormTest(TestCase):
    def setUp(self):
        self.corso1 = Corso.objects.create(
            idcorso='123',
            nome='Corso Test 1',
            categoria='Test',
            descrizione='Descrizione Test',
            durata=60
        )
        self.corso2 = Corso.objects.create(
            idcorso='456',
            nome='Corso Test 2',
            categoria='Test',
            descrizione='Descrizione Test',
            durata=60
        )
        self.sessione1 = SessioneCorso.objects.create(
            fk_corso=self.corso1,
            data='2024-07-01',
            ora='10:00:00',
            sala_corso=1,
            disponibilita=30
        )
        self.sessione2 = SessioneCorso.objects.create(
            fk_corso=self.corso1,
            data='2024-07-01',
            ora='10:00:00',
            sala_corso=2,
            disponibilita=30
        )

    def test_sessione_dublicata(self):
        form_data = {
            'fk_corso': self.corso1.idcorso,
            'data': '2024-07-01',
            'ora': '10:00:00',
            'sala_corso': 1,
            'disponibilita': 30
        }
        form = CreateSessioneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Una sessione con questo corso, data, ora e aula esiste già.", form.errors['__all__'])

    def test_stassaSala(self):
        form_data = {
            'fk_corso': self.corso2.idcorso,
            'data': '2024-07-01',
            'ora': '10:00:00',
            'sala_corso': 1,
            'disponibilita': 30
        }
        form = CreateSessioneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Un altro corso è già programmato in questa sala, data e ora.", form.errors['__all__'])

    def test_stessoCorsoSalaDiversa(self):
        form_data = {
            'fk_corso': self.corso1.idcorso,
            'data': '2024-07-01',
            'ora': '10:00:00',
            'sala_corso': 3,
            'disponibilita': 30
        }
        form = CreateSessioneForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Questo corso è già programmato in un'altra sala alla stessa data e ora.", form.errors['__all__'])

    def test_sessione_valida(self):
        form_data = {
            'fk_corso': self.corso1.idcorso,
            'data': '2024-07-11',
            'ora': '12:00:00',
            'sala_corso': 5,
            'disponibilita': 30
        }
        form = CreateSessioneForm(data=form_data)
        self.assertTrue(form.is_valid())


#TEST PRENOTAZIONE SESSIONI
class PrenotaSessioneTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = GymUser.objects.create_user(
            username='testuser', email='test@test.it', password='12345', nome='Test', cognome='User',
            codice_fiscale='ABCDEF12G34H567I'
        )
        self.client.login(username='testuser', password='12345')

        # Creare abbonamenti
        self.abbonamento_pc = Abbonamento.objects.create(
            codice_abbonamento='PC001', nome='Pacchetto Corsi', tariffa=100.00, durata_massima=30,
            descrizione='Pacchetto corsi'
        )
        self.abbonamento_pp = Abbonamento.objects.create(
            codice_abbonamento='PP001', nome='Pacchetto Palestra', tariffa=80.00, durata_massima=30,
            descrizione='Pacchetto palestra'
        )
        self.abbonamento_pt = Abbonamento.objects.create(
            codice_abbonamento='PT001', nome='Pacchetto Totale', tariffa=150.00, durata_massima=30,
            descrizione='Pacchetto totale'
        )

        # Creare corso
        self.corso = Corso.objects.create(nome='Yoga', descrizione='Corso di Yoga')

        # Creare sessione
        self.sessione = SessioneCorso.objects.create(
            ora=timezone.now().time(),
            data=timezone.now().date(),
            sala_corso=1,
            disponibilita=5,
            fk_corso=self.corso
        )


    def test_visualizzazione_sessioni_disponibili(self):
        response = self.client.get(reverse('unimoregym:sessioni_disponibili'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, self.sessione.fk_corso.nome)

    def test_prenotazione_fallita_per_mancanza_abbonamenti(self):
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, 'Non hai un abbonamento attivo. Per favore, acquista un abbonamento.')

    def test_prenotazione_fallita_per_abbonamenti_non_validi(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pp)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, 'Non hai un abbonamento che ti permette di fare ciò. Per favore, acquista un abbonamento.')

    def test_prenotazione_fallita_per_mancanza_utilizzi_rimanenti(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc, utilizzi_rimanenti=0)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, 'Non hai più utilizzi. Per favore, acquista un nuovo abbonamento.')

    def test_prenotazione_fallita_per_sessione_gia_prenotata(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc, utilizzi_rimanenti=5)
        PrenotazioneUtenteCorso.objects.create(fk_utente=self.user, fk_sessione=self.sessione)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, 'Hai già prenotato un altro corso nella stessa data e ora.')

    def test_prenotazione_fallita_per_sessione_completa(self):
        self.sessione.disponibilita = 0
        self.sessione.save()
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc, utilizzi_rimanenti=5)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertTemplateUsed(response, 'gym/sessioni_disponibili.html')
        self.assertContains(response, 'Non ci sono più posti disponibili per questa sessione.')

    def test_prenotazione_riuscita(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc, utilizzi_rimanenti=5)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertRedirects(response, reverse('unimoregym:mieprenotazioni'))
        abbonamento_attivo = AbbonamentiAttivi.objects.get(fk_utente=self.user, fk_abbonamento=self.abbonamento_pc)
        self.assertEqual(abbonamento_attivo.utilizzi_rimanenti, 4)
        self.assertEqual(SessioneCorso.objects.get(pk=self.sessione.pk).disponibilita, 4)

    def test_prenotazione_riuscita_con_abbonamento_pt(self):
        AbbonamentiAttivi.objects.create(fk_utente=self.user, fk_abbonamento=self.abbonamento_pt)
        response = self.client.post(reverse('unimoregym:sessioni_disponibili'), {'sessione_id': self.sessione.idSessione})
        self.assertRedirects(response, reverse('unimoregym:mieprenotazioni'))
        abbonamento_attivo = AbbonamentiAttivi.objects.get(fk_utente=self.user, fk_abbonamento=self.abbonamento_pt)
        #self.assertEqual(abbonamento_attivo.utilizzi_rimanenti, 4)
        self.assertEqual(SessioneCorso.objects.get(pk=self.sessione.pk).disponibilita, 4)