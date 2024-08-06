from API import modbus
import serial
import concurrent.futures
import time

from OBJ import bilancia as b
from API import modbus
from API import modbus_strutture as st

timeout_duration = 10

def configure(port, list_add):
    
    lista_bilance = []
    for add in list_add:
        print(f"iniziallizzando id {add}")
        instrument = modbus.Instrument(port, add)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.5
        ogg = b.Bilancia(instrument)
        ogg.set_coil_config()
        lista_bilance.append(ogg)
    
    print(f"create bilance {len(list_add)} / {len(lista_bilance)}")
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
        instrument = modbus.Instrument(port, address)  # port name, slave address (in decimal)
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

def test_connection(instrument: modbus.Instrument):
    instrument.serial.timeout = 0.3
    try:
        register = instrument.read_register(12 , functioncode=3)  # Legge 15 registri a partire dal registro HOLDING_CELL1_MS
        
        connection_dummy = register
        print(connection_dummy)
        instrument.serial.timeout = 0.3
        if connection_dummy != 0:
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



def tare_command(instrument: modbus.Instrument):
    print("Tare command launched")
    start_time = time.time()
    try:
        
        tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
        while(tareCoil==0 and (time.time()-start_time < timeout_duration)):
            instrument.write_bit(st.COIL_TARE_COMMAND, 1)
            tareCoil = instrument.read_bit(st.COIL_TARE_COMMAND, functioncode=1)
        if(tareCoil==0):
            print("Timeout exceeded!")
            return -1
        time.sleep(1)   #BRUTTO: last command succeed
        #Here tare takes place
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
    
def calib_command(weight_kg,  instrument):
    start_time = time.time()
    weight = int(weight_kg * 1000)
    try:
        #Setting the weight
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
        #Here calib takes place
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
    
    
def get_totWeight( instrument):
    try:
        return instrument.read_register(st.HOLDING_PESO_TOT_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_PESO_TOT_LS, functioncode=3)
    except:
        return -1
    
def get_cellWeight( instrument):
    cells = []
    try:
        b1 = instrument.read_register(st.HOLDING_CELL1_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL1_LS, functioncode=3)
        b2 = instrument.read_register(st.HOLDING_CELL2_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL2_LS, functioncode=3)
        b3 = instrument.read_register(st.HOLDING_CELL3_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL3_LS, functioncode=3)
        b4 = instrument.read_register(st.HOLDING_CELL4_MS, functioncode=3)*65536 + instrument.read_register(st.HOLDING_CELL4_LS, functioncode=3)
        cells.append(b1)
        cells.append(b2)
        cells.append(b3)
        cells.append(b4)
        return cells
    except:
        return -1
    
def get_cells_status(instrument):
    try:
        return instrument.read_bit(st.COIL_CELL_STATUS, functioncode=1)
    except:
        return -1
    
def get_adcs_status(instrument):
    try:
        return instrument.read_bit(st.COIL_ADCS_STATUS, functioncode=1)
    except:
        return -1