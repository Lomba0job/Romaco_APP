
import serial
import concurrent.futures

from OBJ import bilancia as b
from API import modbus_strutture as st
from API import modbus

def set_accensione(modbus: modbus.Instrument):
    
    
    # print(modbus.address)
    coil_reg = read_coil(modbus)
    print("Coil PRIMA\t|\t", coil_reg)
    modbus.serial.timeout = 2
    modbus.write_bit(st.COIL_CONFIG, value=0, functioncode=5)
    # modbus.write_bit(st.COIL_TARE_COMMAND, value=1, functioncode=5)
    modbus.serial.timeout = 1
    coil_reg = read_coil(modbus)
    print("Coil DOPO\t|\t", coil_reg)
    # print("\n\n")



def read_coil(instrument: modbus.Instrument):
    try:
        modbus.serial.timeout = 0.2
        coils = instrument.read_bit(st.COIL_CONFIG, functioncode=1)
        
        return coils
    except Exception as e:
        print(f"Error reading coil: {e}")
        return None