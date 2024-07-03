from rest_framework import serializers
from unimoregym.models import PrenotazioneUtenteCorso, AbbonamentiAttivi

class PrenotazioneUtenteCorsoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrenotazioneUtenteCorso
        fields = ['idPrenotazione', 'fk_sessione', 'data_prenotazione']

class AbbonamentiAttiviSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbbonamentiAttivi
        fields = ['idabbonamento', 'fk_abbonamento', 'data_prenotazione', 'qr_abbonamento']

class RecommendedCourseSerializer(serializers.Serializer):
    course_name = serializers.CharField(max_length=255)