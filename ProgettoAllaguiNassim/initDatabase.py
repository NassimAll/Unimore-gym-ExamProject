from datetime import time, datetime

from unimoregym.models import *
import decimal

def erase_db():
    print("Cancello il DB")
    Abbonamento.objects.all().delete()
    Trainer.objects.all().delete()
    Corso.objects.all().delete()


def init_db():
    erase_db()
    # Popola gli abbonamenti
    abbonamenti = [
        {
            'codice_abbonamento': 'PP001',
            'nome': 'Sala Pesi - Mensile',
            'tariffa': decimal.Decimal('50.00'),
            'durata_massima': 30,
            'descrizione': 'Accesso in sala pesi per un mese.'
        },
        {
            'codice_abbonamento': 'PP002',
            'nome': 'Sala Pesi - Trimestrale',
            'tariffa': decimal.Decimal('135.00'),
            'durata_massima': 90,
            'descrizione': 'Accesso in sala pesi per tre mesi.'
        },
        {
            'codice_abbonamento': 'PP003',
            'nome': 'Sala Pesi - Annuale',
            'tariffa': decimal.Decimal('500.00'),
            'durata_massima': 365,
            'descrizione': 'Accesso in sala pesi per un anno.'
        },
        {
            'codice_abbonamento': 'PT001',
            'nome': 'Sala Pesi + Corsi - Mensile',
            'tariffa': decimal.Decimal('70.00'),
            'durata_massima': 30,
            'descrizione': 'Accesso illimitato per un mese.'
        },
        {
            'codice_abbonamento': 'PT002',
            'nome': 'Sala Pesi + Corsi - Trimestrale',
            'tariffa': decimal.Decimal('200.00'),
            'durata_massima': 90,
            'descrizione': 'Accesso illimitato per tre mesi.'
        },
        {
            'codice_abbonamento': 'PT003',
            'nome': 'Sala Pesi + Corsi - Annuale',
            'tariffa': decimal.Decimal('600.00'),
            'durata_massima': 365,
            'descrizione': 'Accesso illimitato per un anno.'
        },
        {
            'codice_abbonamento': 'PC001',
            'nome': 'Pacchetto 10 corsi',
            'tariffa': decimal.Decimal('50.00'),
            'durata_massima': 10,
            'descrizione': 'Possibilita di prenotare liberamente fino a 10 corsi, poi rinnovare '
        },
        {
            'codice_abbonamento': 'PC001',
            'nome': 'Pacchetto 10 corsi',
            'tariffa': decimal.Decimal('50.00'),
            'durata_massima': 10,
            'descrizione': 'Possibilita di prenotare liberamente fino a 10 corsi, poi rinnovare '
        },
        {
            'codice_abbonamento': 'PC002',
            'nome': 'Pacchetto 20 corsi',
            'tariffa': decimal.Decimal('100.00'),
            'durata_massima': 20,
            'descrizione': 'Possibilita di prenotare liberamente fino a 20 corsi, poi rinnovare '
        },
        {
            'codice_abbonamento': 'PC003',
            'nome': 'Pacchetto 30 corsi',
            'tariffa': decimal.Decimal('150.00'),
            'durata_massima': 30,
            'descrizione': 'Possibilita di prenotare liberamente fino a 30 corsi, poi rinnovare '
        },
    ]

    for abbonamento_data in abbonamenti:
        a = Abbonamento()
        a.codice_abbonamento = abbonamento_data['codice_abbonamento']
        a.nome = abbonamento_data['nome']
        a.tariffa = abbonamento_data['tariffa']
        a.durata_massima = abbonamento_data['durata_massima']
        a.descrizione = abbonamento_data['descrizione']
        a.save()

    # Popola i trainer
    trainers = [
        {
            'idtrainer': 'T1',
            'nome': 'Mario',
            'cognome': 'Rossi',
            'descrizione': 'Esperto in body building e fitness.'
        },
        {
            'idtrainer': 'T2',
            'nome': 'Luca',
            'cognome': 'Bianchi',
            'descrizione': 'Specialista in yoga e pilates.'
        },
        {
            'idtrainer': 'T3',
            'nome': 'Giulia',
            'cognome': 'Verdi',
            'descrizione': 'Istruttrice di spinning e aerobica.'
        },
        {
            'idtrainer': 'T4',
            'nome': 'Giovanni',
            'cognome': 'Rossi',
            'descrizione': 'Esperto di HIIT .'
        },
        {
            'idtrainer': 'T5',
            'nome': 'Paolo',
            'cognome': 'Davoli',
            'descrizione': 'Atleta di kickboxing.'
        },
        {
            'idtrainer': 'T6',
            'nome': 'Camilla',
            'cognome': 'Verdi',
            'descrizione': 'Istruttrice di Dance fitness'
        },
        {
            'idtrainer': 'T7',
            'nome': 'Andrea',
            'cognome': 'Rossi',
            'descrizione': 'Esperto di body combat'
        },
        {
            'idtrainer': 'T8',
            'nome': 'Luca',
            'cognome': 'Brevini',
            'descrizione': 'Allenatore di crossfit.'
        },
        {
            'idtrainer': 'T9',
            'nome': 'Nicola',
            'cognome': 'Verdi',
            'descrizione': 'Allenatore di body pump.'
        },
        {
            'idtrainer': 'T10',
            'nome': 'Marco',
            'cognome': 'Rossi',
            'descrizione': 'Personal Trainer.'
        },
        {
            'idtrainer': 'T11',
            'nome': 'Luca',
            'cognome': 'Bianchi',
            'descrizione': 'Allenatore di functional training.'
        },
        {
            'idtrainer': 'T12',
            'nome': 'Federica',
            'cognome': 'Pellegrini',
            'descrizione': 'Istruttrice di aquagym.'
        },
        {
            'idtrainer': 'T13',
            'nome': 'Giovanni',
            'cognome': 'Bruno',
            'descrizione': 'Allenatore di TRX.'
        },
        {
            'idtrainer': 'T14',
            'nome': 'Mattia',
            'cognome': 'Ferrari',
            'descrizione': 'Istruttrore di karate.'
        },
        {
            'idtrainer': 'T15',
            'nome': 'Andrea',
            'cognome': 'Cecchi',
            'descrizione': 'Istruttrore di boxe.'
        },
        {
            'idtrainer': 'T16',
            'nome': 'Aldo',
            'cognome': 'Moro',
            'descrizione': 'Istruttrore di taekwondo.'
        },
        {
            'idtrainer': 'T17',
            'nome': 'Sebastian',
            'cognome': 'Bianchi',
            'descrizione': 'Allenatore di Hip Hop.'
        },
        {
            'idtrainer': 'T18',
            'nome': 'Paride',
            'cognome': 'Stomeo',
            'descrizione': 'Istruttrore di Stretching.'
        },
        {
            'idtrainer': 'T19',
            'nome': 'Margherita',
            'cognome': 'Davoli',
            'descrizione': 'Istruttrice di Barre.'
        },
        {
            'idtrainer': 'T20',
            'nome': 'Daniele',
            'cognome': 'Adani',
            'descrizione': 'Personal Trainer'
        },
        {
            'idtrainer': 'T21',
            'nome': 'Paolo',
            'cognome': 'Piccoli',
            'descrizione': 'Trainer di resistenza'
        },
        {
            'idtrainer': 'T22',
            'nome': 'Alessandro',
            'cognome': 'Ligenti',
            'descrizione': 'Trainer di boot camp'
        },
    ]



    # Popola i corsi
    corsi = [
        {
            'idcorso': 'C001',
            'nome': 'Yoga per principianti',
            'categoria': 'Benessere mentale',
            'descrizione': 'Corso di yoga per chi è alle prime armi.',
            'fk_trainer': '2'
        },
        {
            'idcorso': 'C002',
            'nome': 'Spinning avanzato',
            'categoria': 'Aerobica',
            'descrizione': 'Lezione di spinning per avanzati.',
            'fk_trainer': '3'
        },
        {
            'idcorso': 'C003',
            'nome': 'Body Building',
            'categoria': 'Forza',
            'descrizione': 'Corso intensivo di body building.',
            'fk_trainer': '7'
        },
        {
            'idcorso': 'C004',
            'nome': 'Spinning Base',
            'categoria': 'Aerobica',
            'descrizione': 'Lezione di spinning per persone alle prime armi.',
            'fk_trainer': '3'
        },
        {
            'idcorso': 'C005',
            'nome': 'Yoga',
            'categoria': 'Benessere mentale',
            'descrizione': 'Corso di yoga .',
            'fk_trainer': '3'
        },
        {
            'idcorso': 'C006',
            'nome': 'Zumba',
            'categoria': 'Danza',
            'descrizione': 'Una lezione di fitness basata su movimenti di danza latino-americana. È divertente e ottima per bruciare calorie..',
            'fk_trainer': '6'
        },
        {
            'idcorso': 'C007',
            'nome': 'Body Pump',
            'categoria': 'Forza',
            'descrizione': 'Un allenamento di resistenza che utilizza pesi leggeri e ripetizioni elevate per tonificare il corpo.',
            'fk_trainer': '9'
        },
        {
            'idcorso': 'C008',
            'nome': 'CrossFit',
            'categoria': 'Alta-Intensità',
            'descrizione': 'Un programma di allenamento ad alta intensità che combina sollevamento pesi, ginnastica e cardio.',
            'fk_trainer': '8'
        },
        {
            'idcorso': 'C009',
            'nome': 'HIIT',
            'categoria': 'Alta Intensità',
            'descrizione': 'Brevi sessioni di esercizi ad alta intensità intervallate da periodi di riposo o esercizi a bassa intensità.',
            'fk_trainer': '4'
        },
        {
            'idcorso': 'C010',
            'nome': 'Kickboxing - base',
            'categoria': 'Arti marziali',
            'descrizione': 'Combina tecniche di boxe e calci per un allenamento cardiovascolare e di resistenza.',
            'fk_trainer': '5'
        },
        {
            'idcorso': 'C011',
            'nome': 'Kickboxing - avanzato',
            'categoria': 'Arti marziali',
            'descrizione': 'Per quelli con già esperienza. Combina tecniche di boxe e calci per un allenamento cardiovascolare e di resistenza.',
            'fk_trainer': '5'
        },
        {
            'idcorso': 'C012',
            'nome': 'Step Aerobics',
            'categoria': 'Aerobica',
            'descrizione': 'Un allenamento aerobico che utilizza una piattaforma rialzata, noto per migliorare il cardio e la forza delle gambe.',
            'fk_trainer': '3'
        },
        {
            'idcorso': 'C013',
            'nome': 'Aquagym - base',
            'categoria': 'Acquafitness',
            'descrizione': 'Allenamento in acqua che è a basso impatto ma efficace per tonificare i muscoli e migliorare la resistenza cardiovascolare.',
            'fk_trainer': '13'
        },
        {
            'idcorso': 'C014',
            'nome': 'Aquagym - avanzato',
            'categoria': 'Acquafitness',
            'descrizione': 'Allenamento in acqua che è a basso impatto ma efficace per tonificare i muscoli e migliorare la resistenza cardiovascolare.',
            'fk_trainer': '13'
        },
        {
            'idcorso': 'C015',
            'nome': 'Functional Training',
            'categoria': 'Mobilità',
            'descrizione': 'Allenamento che si concentra su movimenti che imitano le attività quotidiane per migliorare la funzionalità generale del corpo.',
            'fk_trainer': '12'
        },
        {
            'idcorso': 'C016',
            'nome': 'TRX (Total Resistance Exercises)',
            'categoria': 'Resistenza',
            'descrizione': 'Allenamento in sospensione che utilizza cinghie per sfruttare il peso del corpo e migliorare forza, equilibrio e flessibilità.',
            'fk_trainer': '22'
        },
        {
            'idcorso': 'C017',
            'nome': 'Circuit Training',
            'categoria': 'Resistenza',
            'descrizione': 'Un allenamento che prevede il passaggio tra diverse stazioni di esercizi, migliorando forza e resistenza cardiovascolare.',
            'fk_trainer': '22'
        },
        {
            'idcorso': 'C018',
            'nome': 'Boot Camp',
            'categoria': 'Alta Intensità',
            'descrizione': 'Allenamento ad alta intensità che combina esercizi militari con movimenti funzionali e cardio.',
            'fk_trainer': '22'
        },
        {
            'idcorso': 'C019',
            'nome': 'Dance fitness - Hip Hop',
            'categoria': 'Danza',
            'descrizione': 'Include vari stili di danza come hip-hop, salsa, jazzercise, che rendono divertente e coinvolgente.',
            'fk_trainer': '18'
        },
        {
            'idcorso': 'C020',
            'nome': 'Dance fitness - Salsa',
            'categoria': 'Danza',
            'descrizione': 'Include vari stili di danza come hip-hop, salsa, jazzercise, che rendono divertente e coinvolgente.',
            'fk_trainer': '6'
        },
        {
            'idcorso': 'C021',
            'nome': 'Barre',
            'categoria': 'Tonificazione',
            'descrizione': 'Combina elementi di balletto, Pilates e yoga per tonificare i muscoli, migliorare la postura e aumentare la flessibilità',
            'fk_trainer': '20'
        },
        {
            'idcorso': 'C022',
            'nome': 'Stretching',
            'categoria': 'Mobilità',
            'descrizione': 'Sessioni focalizzate sull\'allungamento dei muscoli per migliorare la flessibilità e prevenire infortuni.',
            'fk_trainer': '19'
        },
        {
            'idcorso': 'C023',
            'nome': 'Personal Training',
            'categoria': 'Forza',
            'descrizione': 'Sessioni individuali con un allenatore che sviluppa un programma di allenamento personalizzato in base agli obiettivi del cliente.',
            'fk_trainer': '11'
        },
        {
            'idcorso': 'C024',
            'nome': 'Small Group Training',
            'categoria': 'Gruppo',
            'descrizione': 'Allenamenti in piccoli gruppi che combinano l\'attenzione personalizzata con la motivazione di un gruppo..',
            'fk_trainer': '19'
        },
        {
            'idcorso': 'C025',
            'nome': 'Body Combat - karate',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': '15'
        },
        {
            'idcorso': 'C026',
            'nome': 'Body Combat - Boxe',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': '16'
        },
        {
            'idcorso': 'C027',
            'nome': 'Body Combat - taekwondo',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': '17'
        },
    ]

    for trainer_data in trainers:
        t = Trainer()
        t.nome = trainer_data['nome']
        t.cognome = trainer_data['cognome']
        t.descrizione = trainer_data['descrizione']
        t.save()

    trainers = Trainer.objects.all()

    for corso_data in corsi:
        #fk_trainer = Trainer.objects.get(idtrainer=corso_data["fk_trainer"])
        c = Corso()
        c.idcorso = corso_data['idcorso']
        c.nome = corso_data['nome']
        c.categoria = corso_data['categoria']
        c.descrizione = corso_data['descrizione']
        #print((int(corso_data["fk_trainer"])-2))
        c.fk_trainer = trainers[(int(corso_data["fk_trainer"])-2)]
        c.save()


    # Popola sessioni
    sessioni = [
        {
            'data':datetime.date.today(),
            'ora': time(10, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': "C001"
        },
        {
            'data': datetime.date.today(),
            'ora': time(11, 0),
            'sala_corso': 2,
            'disponibilita': 20,
            'fk_corso': 'C002'
        },
        {
            'data': datetime.date.today(),
            'ora': time(12, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C003'
        },
        {
            'data': datetime.date.today(),
            'ora': time(17, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C004'
        },
        {
            'data': datetime.date.today(),
            'ora': time(15, 0),
            'sala_corso': 3,
            'disponibilita': 15,
            'fk_corso': 'C005'
        },
        {
            'data': datetime.date.today() + timedelta(days=1),
            'ora': time(12, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C010'
        },
        {
            'data': datetime.date.today() + timedelta(days=3),
            'ora': time(17, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C011'
        },
        {
            'data': datetime.date.today() + timedelta(days=4),
            'ora': time(11, 0),
            'sala_corso': 2,
            'disponibilita': 10,
            'fk_corso': 'C021'
        },
        {
            'data': datetime.date.today() + timedelta(days=10),
            'ora': time(12, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C016'
        },
        {
            'data': datetime.date.today() + timedelta(days=3),
            'ora': time(11, 0),
            'sala_corso': 1,
            'disponibilita': 30,
            'fk_corso': 'C007'
        },
        {
            'data': datetime.date.today() + timedelta(days=7),
            'ora': time(15, 0),
            'sala_corso': 1,
            'disponibilita': 15,
            'fk_corso': "C014"
        },
        {
            'data': datetime.date.today() + timedelta(days=15),
            'ora': time(11, 0),
            'sala_corso': 7,
            'disponibilita': 30,
            'fk_corso': 'C010'
        },
        {
            'data': datetime.date.today() + timedelta(days=7),
            'ora': time(18, 0),
            'sala_corso': 9,
            'disponibilita': 15,
            'fk_corso': "C010"
        },

    ]

    for sessione in sessioni:
        fk_corso = Corso.objects.get(idcorso=sessione["fk_corso"])
        #print(fk_corso)
        s = SessioneCorso()
        s.data = sessione['data']
        s.ora = sessione['ora']
        s.sala_corso = sessione['sala_corso']
        s.disponibilita = sessione['disponibilita']
        s.fk_corso = fk_corso
        s.save()

    print("DUMP DB")
    print(Corso.objects.all())  # controlliamo
    print(Abbonamento.objects.all())