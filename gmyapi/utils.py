from unimoregym.models import PrenotazioneUtenteCorso

#LISTA DEI CORSI AFFINI TRA DI LORO
MAPPA_CORSI_AFFINI = {
    'Zumba': ['Dance fitness - Salsa', 'Dance fitness - Hip Hop', 'Spinning'],
    'Dance fitness - Salsa': ['Zumba', 'Hip Hop',' Functional Training'],
    'Dance fitness - Hip Hop': ['Zumba', 'Dance fitness - Salsa',' Functional Training'],
    'CrossFit': ['HIIT', 'Boot Camp', 'Stretching'],
    'HIIT': ['CrossFit', 'Boot Camp', 'Stretching'],
    'Boot Camp': ['CrossFit', 'HIIT', 'Stretching'],
    'Spinning Base': ['CrossFit', 'Step Aerobics',' Functional Training'],
    'Spinning avanzato': ['CrossFit', 'Step Aerobics',' Functional Training'],
    'Stretching': ['Personal Training', 'Circuit Training', ' Functional Training'],
    'Step Aerobics': ['Personal Training', 'TRX (Total Resistance Exercises)', ' Functional Training'],
    'Personal Training': ['Body Building', 'Body Pump', 'Stretching'],
    'Body Pump': ['Body Building', 'Functional Training', 'Stretching'],
    'Aquagym - base': ['Personal Training', 'Functional Training', 'Yoga'],
    'Aquagym - avanzato': ['Personal Training', 'Functional Training', 'Yoga'],
    'Yoga': ['Personal Training', 'Barre', 'Stretching'],
    'Yoga per principianti': ['Personal Training', 'Barre', 'Stretching'],
    'Barre': ['Personal Training', 'Yoga', 'Zumba'],
    'Body Building': ['Personal Training', 'Stretching', 'Functional Training'],
    'Kickboxing - avanzato': ['Personal Training', 'Functional Training', 'Body Pump'],
    'Kickboxing - base': ['Personal Training', 'Stretching', 'Functional Training'],
    'Small Group Training': ['Zumba', 'CrossFit', 'Functional Training'],
    'Body Combat - Boxe': ['Personal Training', 'Functional Training', 'Body Pump'],
    'Body Combat - karate': ['Personal Training', 'Body Pump', 'Functional Training'],
    'Body Combat - taekwondo': ['Personal Training', 'Body Pump', 'Functional Training'],
    'Functional Training': ['Personal Training', 'Stretching', 'Spinning avanzato'],
    'TRX (Total Resistance Exercises)': ['Personal Training', 'Stretching', 'Step Aerobics']

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
    print(recommendations)
    return recommendations
