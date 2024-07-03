from unimoregym.models import PrenotazioneUtenteCorso

#LISTA DEI CORSI AFFINI TRA DI LORO
MAPPA_CORSI_AFFINI = {
    'Zumba': ['Dance fitness - Salsa', 'Dance fitness - Hip Hop', 'Spinning'],
    'Dance fitness - Salsa': ['Zumba', 'Hip Hop',' Functional Training'],
    'Dance fitness - Hip Hop': ['Zumba', 'Dance fitness - Salsa',' Functional Training'],
    'CrossFit': ['HIIT', 'Boot Camp', 'Stretching'],
    'HIIT': ['CrossFit', 'Boot Camp', 'Stretching'],
    'Boot Camp': ['CrossFit', 'HIIT', 'Stretching'],
    'Spinning': ['CrossFit', 'Step Aerobics',' Functional Training'],
    'Stretching': ['Personal Trainig', 'Circuit Training', ' Functional Training'],
    'Step Aerobics': ['Personal Trainig', 'TRX (Total Resistance Exercises)', ' Functional Training'],
    'Personal Trainig': ['Body Building', 'Body Pump', 'Stretching'],
    'Body Pump': ['Body Building', 'Functional Training', 'Stretching'],
    'Aquagym': ['Personal Trainig', 'Functional Training', 'Yoga'],
    'Yoga': ['Personal Trainig', 'Barre', 'Stretching'],
    'Barre': ['Personal Trainig', 'Yoga', 'Zumba'],
    'Body Building': ['Personal Trainig', 'Stretching', 'Functional Training']
    # Altre possibilità non sono stato a metterle tutte
}

def get_user_corsi(user): #PRENDO I CORSI DI UN UTENTE
    sessioni_prenotate = PrenotazioneUtenteCorso.objects.filter(fk_utente=user).select_related('fk_sessione__fk_corso')
    corsi_prenotati = {sessione.fk_sessione.fk_corso.nome for sessione in sessioni_prenotate}
    return corsi_prenotati

def recommend_corsi(user):
    booked_courses = get_user_corsi(user)
    recommendations = {} # dizionatio con corsi e suggeriti allegati

    for course in booked_courses:
        if course in MAPPA_CORSI_AFFINI:
            recommended = MAPPA_CORSI_AFFINI[course]
            # Rimuoviamo i corsi già prenotati dall'utente
            recommended = [c for c in recommended if c not in booked_courses]
            recommendations[course] = recommended

    return recommendations
