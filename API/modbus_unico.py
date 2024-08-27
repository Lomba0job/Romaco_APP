
import serial
import concurrent.futures

from OBJ import bilancia as b
from API import modbus_strutture as st
from API import modbus
from API import LOG as l 

def set_accensione(modbus: modbus.Instrument):
    
    try:
        # print(modbus.address)
        coil_reg = read_coil(modbus)
        modbus.serial.timeout = 0.5
        modbus.write_bit(st.COIL_START, value=1, functioncode=5)
        coil_reg = read_coil(modbus)
        l.log_file(14, f"id {modbus.address}")
        return 1
    
    except Exception as e:
        l.log_file(420, f"{e}")
        return 0



def read_coil(instrument: modbus.Instrument):
    try:
        modbus.serial.timeout = 0.2
        coils = instrument.read_bit(st.COIL_CONFIG, functioncode=1)
        return coils
    except Exception as e:
        l.log_file(420, f"{e}")
        return None