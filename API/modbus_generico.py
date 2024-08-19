import threading
from API import modbus
from queue import Queue
import serial
import functools
import concurrent.futures
import time

from OBJ import bilancia as b
from API import modbus
from API import modbus_strutture as st

# Durata timeout
timeout_duration = 10

# Mantieni il lock esistente
_modbus_lock = threading.Lock()

# Crea una coda per le richieste in sospeso
_request_queue = Queue()

# Crea un ThreadPoolExecutor per gestire le richieste
_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def async_modbus_operation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = _thread_pool.submit(_execute_modbus_operation, func, *args, **kwargs)
        return future
    return wrapper

def _execute_modbus_operation(func, *args, **kwargs):
    with _modbus_lock:
        return func(*args, **kwargs)

def configure(port, list_add):
    """
    Configura e inizializza una lista di bilance collegate via Modbus.

    Args:
        port (str): La porta seriale a cui sono collegate le bilance.
        list_add (list): Lista di indirizzi Modbus delle bilance.

    Returns:
        list: Una lista di oggetti Bilancia configurati.
    """
    lista_bilance = []
    for add in list_add:
        print(f"Inizializzando ID {add}")
        instrument = modbus.Instrument(port, add)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.5
        ogg = b.Bilancia(instrument)
        ogg.set_coil_config()
        lista_bilance.append(ogg)
    
    print(f"Bilance create {len(list_add)} / {len(lista_bilance)}")
    return lista_bilance

def connect_modbus(port, address, baud):
    """
    Stabilisce una connessione Modbus con un dispositivo.

    Args:
        port (str): La porta seriale.
        address (int): L'indirizzo del dispositivo Modbus.
        baud (int): Il baud rate per la connessione.

    Returns:
        int: 0 se la connessione è stabilita correttamente, -1 in caso di errore.
    """
    instrument = None
    try:
        print(f"DEBUG| {port} {address}")
        instrument = modbus.Instrument(port, address)  # Nome porta, indirizzo slave (in decimale)
        instrument.serial.baudrate = baud
        instrument.serial.timeout = 0.3
        instrument.mode = modbus.MODE_RTU
        if test_connection(instrument) == 0:
            return 0
        else:
            return -1
    except serial.SerialException as e:
        print(f"Errore di connessione seriale: {e}")
        return -1
    except Exception as e:
        print(f"Errore generico: {e}")
        return -1
    finally:
        if instrument is not None:
            instrument.serial.close()

def test_connection(instrument):
    """
    Testa la connessione con un dispositivo Modbus leggendo un registro.

    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus da testare.

    Returns:
        int: 0 se il test ha successo, -1 o -2 in caso di errore.
    """
    try:
        with _modbus_lock:
            instrument.serial.timeout = 0.3
            register = instrument.read_register(12, functioncode=3)  # Legge registri
            print(register)
            if register != 0:
                return 0
            else:
                return -1
    except Exception as e:
        print(f"Errore nel test di connessione: {e}, indirizzo {instrument.address}")
        return -2
    finally:
        instrument.serial.close()

def check_address(port, address):
    """
    Controlla se un dispositivo Modbus è presente all'indirizzo specificato.

    Args:
        port (str): La porta seriale.
        address (int): L'indirizzo Modbus da controllare.

    Returns:
        int: L'indirizzo se il dispositivo risponde, None altrimenti.
    """
    try:
        response = connect_modbus(port, address, 9600)
        if response == 0:
            return address
    except Exception as e:
        print(f"Errore di comunicazione Modbus con ID {address}: {e}")
    return None

def scan_modbus_network(port):
    """
    Scansiona una rete Modbus per identificare dispositivi attivi.

    Args:
        port (str): La porta seriale da scansionare.

    Returns:
        list: Una lista di ID Modbus di dispositivi attivi.
    """
    connected_ids = []
    print(port)
    for i in range(1, 8):
        print(i)
        r = check_address(port, i)
        if r is not None:
            connected_ids.append(r)
    for id in connected_ids:
        print(id)
    return connected_ids

@async_modbus_operation
def tare_command(instrument: modbus.Instrument):
    """
    Invia il comando di tara al dispositivo Modbus e attende il completamento.

    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus su cui eseguire il comando.

    Returns:
        int: 0 se il comando ha successo, -1 in caso di errore.
    """
    print("Tare command launched")
    start_time = time.time()
    try:
        with _modbus_lock:
            tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
            while(tareCoil==0 and (time.time()-start_time < timeout_duration)):
                instrument.write_bit(st.COIL_TARE_COMMAND, 1)
                tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
            if(tareCoil==0):
                print("Timeout exceeded!")
                return -1
            time.sleep(1)   #BRUTTO: last command succeed
            # Here tare takes place
            tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
            while(tareCoil==1 and (time.time()-start_time < timeout_duration)):
                instrument.write_bit(st.COIL_TARE_COMMAND, 0)
                tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
            if(tareCoil==1):
                print("Timeout exceeded!")
                return -1
            return 0
    except Exception as e:
        print(e)
        return -1
   
@async_modbus_operation 
def calib_command(weight_kg, instrument: modbus.Instrument):
    """
    Esegue il comando di calibrazione impostando un peso specifico e attende il completamento.

    Args:
        weight_kg (float): Il peso in chilogrammi da calibrare.
        instrument (modbus.Instrument): Il dispositivo Modbus su cui eseguire il comando.

    Returns:
        int: 0 se il comando ha successo, -1 in caso di errore.
    """
    start_time = time.time()
    weight = int(weight_kg * 1000)
    try:
        with _modbus_lock:
            # Setting the weight
            calibWeight = instrument.read_register(st.HOLDING_PESO_CALIB_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_PESO_CALIB_LS, functioncode=3)
            while(calibWeight!=weight and (time.time()-start_time < timeout_duration)):
                LS16bit = weight & 0xffff
                MS16bit = (weight >> 16) & 0xffff
                instrument.write_registers(st.HOLDING_PESO_CALIB_MS, [MS16bit, LS16bit]) 
                instrument.write_register(st.HOLDING_PESO_CALIB_MS, MS16bit, functioncode=6)  
                instrument.write_register(st.HOLDING_PESO_CALIB_LS, LS16bit, functioncode=6)  
                
                calibWeight = instrument.read_register(st.HOLDING_PESO_CALIB_MS)* 65536 + instrument.read_register(st.HOLDING_PESO_CALIB_LS, functioncode=3)
                
                t1 = instrument.read_register(st.HOLDING_PESO_CALIB_MS, functioncode=3)* 65536 
                t2 = instrument.read_register(st.HOLDING_PESO_CALIB_LS, functioncode=3)
            if(calibWeight!=weight):
                return -1
            calibCoil = instrument.read_bit(st.COIL_CALIB_COMMAND, functioncode=1)
            while(calibCoil==0 and (time.time()-start_time < timeout_duration)):
                instrument.write_bit(st.COIL_CALIB_COMMAND, 1)
                calibCoil = instrument.read_bit(st.COIL_CALIB_COMMAND, functioncode=1)
            if(calibCoil==0):
                return -1
            time.sleep(2)   #BRUTTO: last command succeed
            # Here calib takes place
            calibCoil = instrument.read_bit(st.COIL_CALIB_COMMAND, functioncode=1)
            while(calibCoil==1 and (time.time()-start_time < timeout_duration)):
                instrument.write_bit(st.COIL_CALIB_COMMAND, 0)
                calibCoil = instrument.read_bit(st.COIL_CALIB_COMMAND, functioncode=1)
            if(calibCoil==1):
                return -1
            return 0
    except Exception as e:
        print(e)
        return -1

    
@async_modbus_operation    
def get_totWeight(instrument: modbus.Instrument):
    """
    Ottiene il peso totale dal dispositivo Modbus.

    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus da cui leggere il peso.

    Returns:
        float: Il peso totale letto, -1 in caso di errore.
    """
    try:
        with _modbus_lock:
            instrument.write_bit(st.COIL_PESO_COMMAND, 1, functioncode=5)
            stato = True
            while stato:
                modbus.serial.timeout = 0.2
                ris = instrument.read_bit(st.COIL_LAST_COMMAND_SUCCESS, functioncode=1)
                if ris == 1:
                    stato = False
            peso = twos_complement_inverse(instrument.read_register(st.HOLDING_PESO_TOT_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_PESO_TOT_LS, functioncode=3), 32)
        return peso
    except:
        return -1
    
def twos_complement_inverse(x, bits):
    """
    Calcola l’inverso del complemento a due di un numero.
    Args:
        x (int): Il numero su cui eseguire il calcolo.
        bits (int): Il numero di bit del complemento a due.

    Returns:
        int: Il valore convertito.
    """
    if bits <= 0:
        raise ValueError("Il numero di bit deve essere maggiore di 0")

    max_value = 2**bits
    if x >= max_value:
        raise ValueError(f"Valore fuori dal range per un numero a {bits} bit")

    if x < 0:
        raise ValueError("L'input deve essere un intero non negativo")

    # Verifica se il numero è nella gamma negativa nel complemento a due
    if x >= 2**(bits - 1):
        x -= 2**bits

    return x
    
@async_modbus_operation   
def get_cellWeight(instrument: modbus.Instrument):
    """
    Ottiene i pesi delle celle dal dispositivo Modbus.    
    
    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus da cui leggere i pesi.

    Returns:
        list: Una lista di pesi delle celle, -1 in caso di errore.
        """
    cells = []
    try:
        with _modbus_lock:
            modbus.serial.timeout = 0.2
            b1 = instrument.read_register(st.HOLDING_CELL1_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL1_LS, functioncode=3)
            b2 = instrument.read_register(st.HOLDING_CELL2_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL2_LS, functioncode=3)
            b3 = instrument.read_register(st.HOLDING_CELL3_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL3_LS, functioncode=3)
            b4 = instrument.read_register(st.HOLDING_CELL4_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL4_LS, functioncode=3)

        b1_int = twos_complement_inverse(b1, 32)
        b2_int = twos_complement_inverse(b2, 32)
        b3_int = twos_complement_inverse(b3, 32)
        b4_int = twos_complement_inverse(b4, 32)
        print(f"DEBUG MODBUS API | {b1} -> {b1_int} ")
        print(f"DEBUG MODBUS API | {b2} -> {b2_int} ")
        print(f"DEBUG MODBUS API | {b3} -> {b3_int} ")
        print(f"DEBUG MODBUS API | {b4} -> {b4_int} ")
        cells.append(b1_int)
        cells.append(b2_int)
        cells.append(b3_int)
        cells.append(b4_int)
        modbus.serial.timeout = 0.2
        return cells
    except:
        return -1

def get_cells_status(instrument: modbus.Instrument):
    """
    Ottiene lo stato delle celle dal dispositivo Modbus.
    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus da cui leggere lo stato delle celle.

    Returns:
        int: Lo stato delle celle, -1 in caso di errore.
    """
    try:
        with _modbus_lock:
            return instrument.read_bit(st.COIL_CELL_STATUS, functioncode=1)
    except:
        return -1

@async_modbus_operation  
def get_adcs_status(instrument: modbus.Instrument):
    """
    Ottiene lo stato degli ADC dal dispositivo Modbus.
    Args:
        instrument (modbus.Instrument): Il dispositivo Modbus da cui leggere lo stato degli ADC.
    
    Returns:
        int: Lo stato degli ADC, -1 in caso di errore.
    """
    try:
        with _modbus_lock:
            return instrument.read_bit(st.COIL_ADCS_STATUS, functioncode=1)
    except:
        return -1