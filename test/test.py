import minimalmodbus
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
instrument = minimalmodbus.Instrument('/dev/tty.usbserial-FT57PLKR', 1)  # Modifica '/dev/ttyUSB0' con il tuo dispositivo seriale e '1' con l'ID del tuo slave
instrument.serial.baudrate = 9600  # Modifica la velocità in baud secondo necessità instrument.serial.bytesize = 8 instrument.serial.parity = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.bytesize = 8
instrument.serial.parity = serial.PARITY_NONE
instrument.serial.timeout = 2  # secondi

instrument.mode = minimalmodbus.MODE_RTU

# Funzioni per leggere i registri holding
def read_holding_registers():
    try:
        registers = instrument.read_registers(0, 15, functioncode=3)  # Legge 15 registri a partire dal registro HOLDING_CELL1_MS
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
    coils = []
    try:
        for i in range(0,9):
            coils.append(instrument.read_bit(i*8 , functioncode=1))  # Legge 8 coil a partire dal coil COIL_PESO_COMMAND
        print(f"Coils read: {coils}")  # Debug
        coil_reg_params = {
            'coil_PesoCommand': coils[0],
            'coil_TareCommand': coils[1],
            'coil_CalibCommand': coils[2],
            'coil_LastCommandSuccess': coils[3],
            'coil_PresenceStatus': coils[4],
            'coil_CellStatus': coils[5],
            'coil_AdcsStatus': coils[6],
            'coil_Config': coils[7],
            'input_state': coils[8]
        }
        return coil_reg_params
    except Exception as e:
        print(f"Error reading coils: {e}")
        return None

    

    



# Esempio di utilizzo della lettura dei registri
holding_regs = read_holding_registers()
print("Holding Registers:", holding_regs)

coil_regs = read_coils()
print("Coil Registers:", coil_regs)

