import threading
import time
from django.utils import timezone
from unimoregym.models import SessioneCorso, AbbonamentiAttivi

class Remove_Scaduti_Thread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        while True:
            self.remove_vecchie_sessioni()
            self.remove_abb_scaduti()
            time.sleep(24 * 60 * 60)  # Esegui ogni 24 ore

    def remove_vecchie_sessioni(self):
        now = timezone.now()
        SessioneCorso.objects.filter(data__lt=now.date()).delete()

    def remove_abb_scaduti(self):
        now = timezone.now()
        AbbonamentiAttivi.objects.filter(data_scadenza__lt=now.date()).delete()

def start_thread():
    th = Remove_Scaduti_Thread()
    th.start()