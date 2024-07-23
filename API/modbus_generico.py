import minimalmodbus
import serial
import concurrent.futures

from OBJ import bilancia as b
from API import modbus_strutture as st

def configure(port, list_add):
    
    lista_bilance = []
    for add in list_add:
        print(f"iniziallizzando id {add}")
        instrument = minimalmodbus.Instrument(port, add)
        ogg = b.Bilancia(instrument)
        lista_bilance.append(ogg)
    
    print(f"temrianto con {len(list_add)} / {len(lista_bilance)}")
    return lista_bilance


def connect_modbus(port, address, baud):
    """Stabilisce connessione modbus
    Args:
        port (string): porta
        address (int): indirizzo
        baud (int): baudrate
    Returns:
        0: connessione stabilita
        -1: connessione non stabilita
    """
    try:
        instrument = minimalmodbus.Instrument(port, address)  # port name, slave address (in decimal)
        instrument.serial.baudrate = baud
        instrument.serial.timeout = 1
        instrument.mode = minimalmodbus.MODE_RTU
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

def test_connection(instrument):
    instrument.serial.timeout = 1
    try:
        registers = instrument.read_registers(0, 15, 3)  # Legge 15 registri a partire dal registro HOLDING_CELL1_MS
        
        connection_dummy = registers[12]
        print(connection_dummy)
        instrument.serial.timeout = 1
        if connection_dummy == 1:
            return 0
        else:
            return -1
    except Exception as e:
        print(f"Errore nel test di connessione: {e}, indirizzo {instrument.address}")
        return -2

def check_address(port, address):
    try:
        response = connect_modbus(port, address, 9600)
        if response == 0:
            return address
    except Exception as e:
        print(f"Errore di comunicazione Modbus con ID {address}: {e}")
    return None

def scan_modbus_network(port):
    connected_ids = []
    print(port)
    
    
    for i in range(1, 8):
        r = check_address(port=port, address=i)
        if r is not None:
            connected_ids.append(r)
    
        
    for id in connected_ids:
        print(id)
    
    return connected_ids

