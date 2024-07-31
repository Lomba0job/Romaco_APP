import sqlite3
from API import funzioni as f

def crea_db():
    # Connessione al database (crea il database se non esiste)
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Creazione della tabella PESATA
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PESATA (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        peso_totale FLOAT,
        peso_b1 FLOAT,
        peso_b2 FLOAT,
        peso_b3 FLOAT,
        peso_b4 FLOAT,
        peso_b5 FLOAT,
        peso_b6 FLOAT,
        desc TEXT,
        priority INTEGER,
        data TEXT
    )
    ''')
    
    # Salvataggio delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()
import sqlite3

def put(peso_tot, b1, b2, b3, b4, b5, b6, desc, prio, data):
    # Connessione al database (crea il database se non esiste)
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    Value = (peso_tot, b1, b2, b3, b4, b5, b6, desc, prio, data)
    
    # Inserimento dei dati nella tabella PESATA
    query = '''
        INSERT INTO PESATA (peso_totale, peso_b1, peso_b2, peso_b3, peso_b4, peso_b5, peso_b6, desc, priority, data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    # Esecuzione della query con i dati
    try:
        cursor.execute(query, Value)
        conn.commit()  # Salvataggio delle modifiche
        conn.close()
        return 0
    except sqlite3.Error as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
        return 1

def get():
    # Connessione al database
    conn = sqlite3.connect('pesata.db')
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Query per ottenere le ultime 100 misure, ordinando per una colonna di riferimento
    query = '''
        SELECT * FROM PESATA ORDER BY rowid DESC LIMIT 100
    '''
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()  # Recupera tutte le righe del risultato della query
        conn.close()
        
        # Nomi delle colonne come chiavi del dizionario
        column_names = ['peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        print(f"Errore durante il recupero dei dati: {e}")
        return []
    
import sqlite3

def get_suc(page_number):
    # Numero di righe per pagina
    page_size = 100
    
    # Calcolo dell'offset
    offset = (page_number - 1) * page_size
    
    # Connessione al database
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Query per ottenere le pesate per la pagina richiesta
    query = '''
        SELECT * FROM PESATA ORDER BY rowid LIMIT ? OFFSET ?
    '''
    
    try:
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()  # Recupera tutte le righe del risultato della query
        conn.close()
        
        # Nomi delle colonne come chiavi del dizionario
        column_names = ['peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        print(f"Errore durante il recupero dei dati: {e}")
        return []