import minimalmodbus
import serial
import concurrent.futures

from OBJ import bilancia as b
# Costanti per i registri holding
HOLDING_CELL1_MS = 0
HOLDING_CELL1_LS = 1
HOLDING_CELL2_MS = 2
HOLDING_CELL2_LS = 3
HOLDING_CELL3_MS = 4
HOLDING_CELL3_LS = 5
HOLDING_CELL4_MS = 6
HOLDING_CELL4_LS = 7
HOLDING_PESO_TOT_MS = 8
HOLDING_PESO_TOT_LS = 9
HOLDING_PESO_CALIB_MS = 10
HOLDING_PESO_CALIB_LS = 11
CONNECTION_DUMMY = 12
COUNT = 13
DIAGNOSTIC = 14

# Costanti per i coil
COIL_PESO_COMMAND = 0
COIL_TARE_COMMAND = 1
COIL_CALIB_COMMAND = 2
COIL_LAST_COMMAND_SUCCESS = 3
COIL_PRESENCE_STATUS = 4
COIL_CELL_STATUS = 5
COIL_ADCS_STATUS = 6
COIL_CONFIG = 7

def configure(port, list_add):
    for add in list_add:
        instrument = minimalmodbus.Instrument(port, add)
        b.Bilancia(instrument)


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
        instrument.serial.timeout = 0.5
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
        connection_dummy = instrument.read_register(CONNECTION_DUMMY)
        instrument.serial.timeout = 0.1
        if connection_dummy == 1:
            return 0
        else:
            return -1
    except Exception as e:
        print(f"Errore nel test di connessione: {e}, indiirzzo {instrument.address}")
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
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(check_address, port, i) for i in range(1, 247)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                connected_ids.append(result)
    
    for id in connected_ids:
        print(id)
    
    return connected_ids

