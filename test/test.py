from API import modbus
import serial

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
COIL_TARE_COMMAND = 8
COIL_CALIB_COMMAND = 16
COIL_LAST_COMMAND_SUCCESS = 24
COIL_PRESENCE_STATUS = 32
COIL_CELL_STATUS = 40
COIL_ADCS_STATUS = 48
COIL_CONFIG = 56



# Indirizzi dei registri input
INPUT_TEST = 0

# Indirizzi dei registri discreti
DISCRETE_TEST = 0

# Definisce la dimensione massima possibile per il numero di scale
MAX_SCALES = 6


# Configurazione del master Modbus
instrument = modbus.Instrument('/dev/tty.usbserial-FT57PLKR', 1)  # Modifica '/dev/ttyUSB0' con il tuo dispositivo seriale e '1' con l'ID del tuo slave
instrument.serial.baudrate = 9600  # Modifica la velocità in baud secondo necessità instrument.serial.bytesize = 8 instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.timeout = 2  # secondi

instrument.mode = modbus.MODE_RTU

# Funzioni per leggere i registri holding
def read_holding_registers():
    try:
        registers = instrument.read_registers(0, 15, 3)  # Legge 15 registri a partire dal registro HOLDING_CELL1_MS
        print(f"Registers read: {registers}")  # Debug
        holding_reg_params = {
            'holding_cell1MS': registers[0],
            'holding_cell1LS': registers[1],
            'holding_cell2MS': registers[2],
            'holding_cell2LS': registers[3],
            'holding_cell3MS': registers[4],
            'holding_cell3LS': registers[5],
            'holding_cell4MS': registers[6],
            'holding_cell4LS': registers[7],
            'holding_pesoTotMS': registers[8],
            'holding_pesoTotLS': registers[9],
            'holding_pesoCalibMS': registers[10],
            'holding_pesoCalibLS': registers[11],
            'connection_dummy': registers[12],
            'count': registers[13],
            'diagnostic': registers[14]
        }
        return holding_reg_params
    except Exception as e:
        print(f"Error reading holding registers: {e}")
        return None

# Funzioni per leggere i coil
def read_coils():
    try:
        coils = instrument.read_bits(0, 8, 1)  # Legge 8 coil a partire dal coil COIL_PESO_COMMAND
        print(f"Coils read: {coils}")  # Debug
        coil_reg_params = {
            'coil_PesoCommand': coils[0],
            'coil_TareCommand': coils[1],
            'coil_CalibCommand': coils[2],
            'coil_LastCommandSuccess': coils[3],
            'coil_PresenceStatus': coils[4],
            'coil_CellStatus': coils[5],
            'coil_AdcsStatus': coils[6],
            'coil_Config': coils[7]
        }
        return coil_reg_params
    except Exception as e:
        print(f"Error reading coils: {e}")
        return None
    
def test_connection():
    try:
        instrument.serial.timeout = 10
        register = instrument.read_register(12, 3)  # Legge il registro con address 12
        print(f"Connection dummy read: {register}, type: {type(register)}")  # Debug
        if isinstance(register, float) and abs(register - 0.001) < 0.0001:
            register = 1  # Trattare 0.001 come 1
        connection_dummy = register
        print(connection_dummy)
        instrument.serial.timeout = 2
        if connection_dummy != 0:
            return 0
        else:
            return -1
    except Exception as e:
        print(f"Errore nel test di connessione: {e}, indirizzo {instrument.address}")
        instrument.serial.timeout = 2
        return -2
    
    
def write():
    instrument.write_register(12, 8)
    instrument.write_register(13, 8)
    instrument.write_register(14, 8)
    
    

Test = test_connection()


# Esempio di utilizzo della lettura dei registri
holding_regs = read_holding_registers()
print("Holding Registers:", holding_regs)

coil_regs = read_coils()
print("Coil Registers:", coil_regs)

write()

Test = test_connection()


# Esempio di utilizzo della lettura dei registri
holding_regs = read_holding_registers()
print("Holding Registers:", holding_regs)

coil_regs = read_coils()
print("Coil Registers:", coil_regs)
"""
Holding Registers: {'holding_cell1MS': 0, 'holding_cell1LS': 0, 'holding_cell2MS': 0, 'holding_cell2LS': 0, 'holding_cell3MS': 0, 'holding_cell3LS': 0, 'holding_cell4MS': 0, 'holding_cell4LS': 0, 'holding_pesoTotMS': 0, 'holding_pesoTotLS': 0, 'holding_pesoCalibMS': 0, 'holding_pesoCalibLS': 0, 'connection_dummy': 1, 'count': 0, 'diagnostic': 0}
Coil Registers: {'coil_PesoCommand': 0, 'coil_TareCommand': 0, 'coil_CalibCommand': 0, 'coil_LastCommandSuccess': 0, 'coil_PresenceStatus': 0, 'coil_CellStatus': 0, 'coil_AdcsStatus': 0, 'coil_Config': 0}
"""