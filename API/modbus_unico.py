
import serial
import concurrent.futures

from OBJ import bilancia as b
from API import modbus_strutture as st
from API import modbus

def set_accensione(modbus: modbus.Instrument):
    
    
    # print(modbus.address)
    coil_reg = read_coil(modbus)
    modbus.serial.timeout = 0.5
    modbus.write_bit(st.COIL_START, value=1, functioncode=5)
    # modbus.write_bit(st.COIL_TARE_COMMAND, value=1, functioncode=5)
    modbus.serial.timeout = 1
    coil_reg = read_coil(modbus)




def read_coil(instrument: modbus.Instrument):
    try:
        modbus.serial.timeout = 1
        coils = instrument.read_bit(st.COIL_CONFIG, functioncode=1)
        
        return coils
    except Exception as e:
        print(f"Error reading coil: {e}")
        return None