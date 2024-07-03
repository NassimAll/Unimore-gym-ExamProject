from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from unimoregym.models import PrenotazioneUtenteCorso, AbbonamentiAttivi
from .serializers import PrenotazioneUtenteCorsoSerializer, AbbonamentiAttiviSerializer, RecommendedCourseSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .utils import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prenotazioni_corsi_utente(request):
    user = request.user
    prenotazioni = PrenotazioneUtenteCorso.objects.filter(fk_utente=user)
    serializer = PrenotazioneUtenteCorsoSerializer(prenotazioni, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def abbonamenti_attivi_utente(request):
    user = request.user
    abbonamenti = AbbonamentiAttivi.objects.filter(fk_utente=user)
    serializer = AbbonamentiAttiviSerializer(abbonamenti, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_corsi_api(request):
    user = request.user
    recommended_courses = recommend_corsi(user)
    return JsonResponse(recommended_courses)
