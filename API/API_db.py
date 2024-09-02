import sqlite3
from API import funzioni as f, LOG as l 

def crea_db():
    l.log_file(111, " creazione")
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
        data TEXT, 
        name TEXT
    )
    ''')
    
    # Salvataggio delle modifiche e chiusura della connessione
    conn.commit()
    conn.close()
import sqlite3

def put(peso_tot, b1, b2, b3, b4, b5, b6, desc, prio, data, nome):
    l.log_file(111, " inserimento")
    # Connessione al database (crea il database se non esiste)
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    Value = (peso_tot, b1, b2, b3, b4, b5, b6, desc, prio, data, nome)
    
    # Inserimento dei dati nella tabella PESATA
    query = '''
        INSERT INTO PESATA (peso_totale, peso_b1, peso_b2, peso_b3, peso_b4, peso_b5, peso_b6, desc, priority, data, name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    # Esecuzione della query con i dati
    try:
        cursor.execute(query, Value)
        conn.commit()  # Salvataggio delle modifiche
        conn.close()
        return 0
    except sqlite3.Error as e:
        l.log_file(419, f" {e}")
        return 1

def get(page_number):
    l.log_file(111, " download")
    # Numero di righe per pagina
    page_size = 100
    
    # Calcolo dell'offset
    offset = (page_number - 1) * page_size if page_number > 0 else 0
    
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
        column_names = ['id', 'peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data', 'name']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        l.log_file(12)
        return results
    except sqlite3.Error as e:
        l.log_file(418, f" {e}")
        return []
    
def get_latest_entries():
    l.log_file(111, " download")
    # Numero di righe da recuperare
    page_size = 100
    
    # Connessione al database
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Query per ottenere gli ultimi 100 record ordinati per id in modo decrescente
    query = '''
        SELECT * FROM PESATA ORDER BY id DESC LIMIT ?
    '''
    
    try:
        cursor.execute(query, (page_size,))
        rows = cursor.fetchall()  # Recupera tutte le righe del risultato della query
        conn.close()
        
        # Nomi delle colonne come chiavi del dizionario
        column_names = ['id', 'peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data', 'name']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        l.log_file(12)
        return results
    except sqlite3.Error as e:
        l.log_file(418, f" {e}")
        return []


def get_priority(page_number, priority):
    l.log_file(111, " download prioritario")
    # Numero di righe per pagina
    page_size = 100
    
    # Calcolo dell'offset
    offset = (page_number - 1) * page_size if page_number > 0 else 0
    
    # Connessione al database
    conn = sqlite3.connect(f.get_db())
    
    # Creazione di un cursore per eseguire i comandi SQL
    cursor = conn.cursor()
    
    # Query per ottenere le pesate per la pagina richiesta, filtrando per priorità
    query = '''
        SELECT * FROM PESATA WHERE priority = ? ORDER BY rowid LIMIT ? OFFSET ?
    '''
    
    try:
        cursor.execute(query, (priority, page_size, offset))
        rows = cursor.fetchall()  # Recupera tutte le righe del risultato della query
        conn.close()
        
        # Nomi delle colonne come chiavi del dizionario
        column_names = ['id', 'peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data', 'name']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        l.log_file(418, f" {e}")
        return []

def get_filtered(page_number, date_from=None, date_to=None, priority=None):
    l.log_file(111, " download filtrato")
    # Numero di righe per pagina
    page_size = 100
    
    # Calcolo dell'offset
    offset = (page_number - 1) * page_size if page_number > 0 else 0
    
    # Connessione al database
    conn = sqlite3.connect(f.get_db())
    cursor = conn.cursor()
    
    # Query di base
    query = 'SELECT * FROM PESATA WHERE 1=1'
    params = []
    
    # Filtro per data
    if date_from:
        query += ' AND data >= ?'
        params.append(date_from)
    if date_to:
        query += ' AND data <= ?'
        params.append(date_to)
    
    # Filtro per priorità
    if priority:
        if isinstance(priority, list):
            placeholders = ','.join('?' for _ in priority)
            query += f' AND priority IN ({placeholders})'
            params.extend(priority)
        else:
            query += ' AND priority = ?'
            params.append(priority)
    
    # Ordinamento e limitazione per pagina
    query += ' ORDER BY rowid LIMIT ? OFFSET ?'
    params.extend([page_size, offset])
    
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Nomi delle colonne come chiavi del dizionario
        column_names = ['id', 'peso_totale', 'peso_b1', 'peso_b2', 'peso_b3', 'peso_b4', 'peso_b5', 'peso_b6', 'desc', 'priority', 'data', 'name']
        
        # Conversione delle righe in una lista di dizionari
        results = [dict(zip(column_names, row)) for row in rows]
        return results
    except sqlite3.Error as e:
        l.log_file(418, f" {e}")
        return []