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
            'nome': 'Mario',
            'cognome': 'Rossi',
            'descrizione': 'Esperto in body building e fitness.'
        },
        {
            'nome': 'Luca',
            'cognome': 'Bianchi',
            'descrizione': 'Specialista in yoga e pilates.'
        },
        {
            'nome': 'Giulia',
            'cognome': 'Verdi',
            'descrizione': 'Istruttrice di spinning e aerobica.'
        },
        {
            'nome': 'Giovanni',
            'cognome': 'Rossi',
            'descrizione': 'Esperto di HIIT .'
        },
        {
            'nome': 'Paolo',
            'cognome': 'Davoli',
            'descrizione': 'Atleta di kickboxing.'
        },
        {
            'nome': 'Camilla',
            'cognome': 'Verdi',
            'descrizione': 'Istruttrice di Dance fitness'
        },
        {
            'nome': 'Andrea',
            'cognome': 'Rossi',
            'descrizione': 'Esperto di body combat'
        },
        {
            'nome': 'Luca',
            'cognome': 'Brevini',
            'descrizione': 'Allenatore di crossfit.'
        },
        {
            'nome': 'Nicola',
            'cognome': 'Verdi',
            'descrizione': 'Allenatore di body pump.'
        },
        {
            'nome': 'Marco',
            'cognome': 'Rossi',
            'descrizione': 'Personal Trainer.'
        },
        {
            'nome': 'Luca',
            'cognome': 'Bianchi',
            'descrizione': 'Allenatore di functional training.'
        },
        {
            'nome': 'Federica',
            'cognome': 'Pellegrini',
            'descrizione': 'Istruttrice di aquagym.'
        },
        {
            'nome': 'Giovanni',
            'cognome': 'Bruno',
            'descrizione': 'Allenatore di TRX.'
        },
        {
            'nome': 'Mattia',
            'cognome': 'Ferrari',
            'descrizione': 'Istruttrore di karate.'
        },
        {
            'nome': 'Andrea',
            'cognome': 'Cecchi',
            'descrizione': 'Istruttrore di boxe.'
        },
        {
            'nome': 'Aldo',
            'cognome': 'Moro',
            'descrizione': 'Istruttrore di taekwondo.'
        },
        {
            'nome': 'Sebastian',
            'cognome': 'Bianchi',
            'descrizione': 'Allenatore di Hip Hop.'
        },
        {
            'nome': 'Matilde',
            'cognome': 'Mussini',
            'descrizione': 'Istruttrore di Stretching.'
        },
        {
            'nome': 'Margherita',
            'cognome': 'Davoli',
            'descrizione': 'Istruttrice di Barre.'
        },
        {
            'nome': 'Daniele',
            'cognome': 'Adani',
            'descrizione': 'Personal Trainer'
        },
    ]

    for trainer_data in trainers:
        t = Trainer()
        t.nome = trainer_data['nome']
        t.cognome = trainer_data['cognome']
        t.descrizione = trainer_data['descrizione']
        t.save()

    # Popola i corsi
    corsi = [
        {
            'idcorso': 'C001',
            'nome': 'Yoga per principianti',
            'categoria': 'Benessere mentale',
            'descrizione': 'Corso di yoga per chi è alle prime armi.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C002',
            'nome': 'Spinning avanzato',
            'categoria': 'Aerobica',
            'descrizione': 'Lezione di spinning per avanzati.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C003',
            'nome': 'Body Building',
            'categoria': 'Forza',
            'descrizione': 'Corso intensivo di body building.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C004',
            'nome': 'Spinning Base',
            'categoria': 'Aerobica',
            'descrizione': 'Lezione di spinning per persone alle prime armi.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C005',
            'nome': 'Yoga',
            'categoria': 'Benessere mentale',
            'descrizione': 'Corso di yoga .',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C006',
            'nome': 'Zumba',
            'categoria': 'Danza',
            'descrizione': 'Una lezione di fitness basata su movimenti di danza latino-americana. È divertente e ottima per bruciare calorie..',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C007',
            'nome': 'Body Pump',
            'categoria': 'Forza',
            'descrizione': 'Un allenamento di resistenza che utilizza pesi leggeri e ripetizioni elevate per tonificare il corpo.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C008',
            'nome': 'CrossFit',
            'categoria': 'Alta-Intensità',
            'descrizione': 'Un programma di allenamento ad alta intensità che combina sollevamento pesi, ginnastica e cardio.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C009',
            'nome': 'HIIT',
            'categoria': 'Alta Intensità',
            'descrizione': 'Brevi sessioni di esercizi ad alta intensità intervallate da periodi di riposo o esercizi a bassa intensità.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C010',
            'nome': 'Kickboxing - base',
            'categoria': 'Arti marziali',
            'descrizione': 'Combina tecniche di boxe e calci per un allenamento cardiovascolare e di resistenza.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C011',
            'nome': 'Kickboxing - avanzato',
            'categoria': 'Arti marziali',
            'descrizione': 'Per quelli con già esperienza. Combina tecniche di boxe e calci per un allenamento cardiovascolare e di resistenza.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C012',
            'nome': 'Step Aerobics',
            'categoria': 'Aerobica',
            'descrizione': 'Un allenamento aerobico che utilizza una piattaforma rialzata, noto per migliorare il cardio e la forza delle gambe.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C013',
            'nome': 'Aquagym - base',
            'categoria': 'Acquafitness',
            'descrizione': 'Allenamento in acqua che è a basso impatto ma efficace per tonificare i muscoli e migliorare la resistenza cardiovascolare.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C014',
            'nome': 'Aquagym - avanzato',
            'categoria': 'Acquafitness',
            'descrizione': 'Allenamento in acqua che è a basso impatto ma efficace per tonificare i muscoli e migliorare la resistenza cardiovascolare.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C015',
            'nome': 'Functional Training',
            'categoria': 'Mobilità',
            'descrizione': 'Allenamento che si concentra su movimenti che imitano le attività quotidiane per migliorare la funzionalità generale del corpo.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C016',
            'nome': 'TRX (Total Resistance Exercises)',
            'categoria': 'Resistenza',
            'descrizione': 'Allenamento in sospensione che utilizza cinghie per sfruttare il peso del corpo e migliorare forza, equilibrio e flessibilità.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C017',
            'nome': 'Circuit Training',
            'categoria': 'Resistenza',
            'descrizione': 'Un allenamento che prevede il passaggio tra diverse stazioni di esercizi, migliorando forza e resistenza cardiovascolare.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C018',
            'nome': 'Boot Camp',
            'categoria': 'Alta Intensità',
            'descrizione': 'Allenamento ad alta intensità che combina esercizi militari con movimenti funzionali e cardio.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C019',
            'nome': 'Dance fitness - Hip Hop',
            'categoria': 'Danza',
            'descrizione': 'Include vari stili di danza come hip-hop, salsa, jazzercise, che rendono divertente e coinvolgente.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C020',
            'nome': 'Dance fitness - Salsa',
            'categoria': 'Danza',
            'descrizione': 'Include vari stili di danza come hip-hop, salsa, jazzercise, che rendono divertente e coinvolgente.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C021',
            'nome': 'Barre',
            'categoria': 'Tonificazione',
            'descrizione': 'Combina elementi di balletto, Pilates e yoga per tonificare i muscoli, migliorare la postura e aumentare la flessibilità',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C022',
            'nome': 'Stretching',
            'categoria': 'Mobilità',
            'descrizione': 'Sessioni focalizzate sull\'allungamento dei muscoli per migliorare la flessibilità e prevenire infortuni.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C023',
            'nome': 'Personal Trainig',
            'categoria': 'Forza',
            'descrizione': 'Sessioni individuali con un allenatore che sviluppa un programma di allenamento personalizzato in base agli obiettivi del cliente.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C024',
            'nome': 'Small Group Training',
            'categoria': 'Gruppo',
            'descrizione': 'Allenamenti in piccoli gruppi che combinano l\'attenzione personalizzata con la motivazione di un gruppo..',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C025',
            'nome': 'Body Combat - karate',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C026',
            'nome': 'Body Combat - Boxe',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': ''
        },
        {
            'idcorso': 'C027',
            'nome': 'Body Combat - taekwondo',
            'categoria': 'Arti Marziali',
            'descrizione': 'Un allenamento cardio ispirato alle arti marziali, che utilizza movimenti di karate, boxe, taekwondo e muay thai.',
            'fk_trainer': ''
        },
    ]

    for corso_data in corsi:
        c = Corso()
        c.idcorso = corso_data['idcorso']
        c.nome = corso_data['nome']
        c.categoria = corso_data['categoria']
        c.descrizione = corso_data['descrizione']
        c.save()

    print("DUMP DB")
    print(Corso.objects.all()) #controlliamo
    print(Abbonamento.objects.all())
