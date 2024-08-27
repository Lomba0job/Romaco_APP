from API import modbus_strutture as st 
from API import modbus_unico as mb
from API import modbus
from API import LOG as l 

class Bilancia():
    
    def __init__(self, modbus_) -> None:
        self.modbusI: modbus.Instrument = modbus_
        self.position = None
        
    def set_coil_config(self) -> None:
        # print(f"Configurazione Bilancia {self.modbusI.address}")
        mb.set_accensione(self.modbusI)
        
        
    def check_coil_status(self) -> int:
        coil = mb.read_coil(self.modbusI)
        if coil == 1:
            message = f"Bilancia N {self.modbusI.address} ha riportato la bilancia a 1"
            # print(message)
            return 1
        else:
            message = f"Bilancia N {self.modbusI.address} non identificata"
            # print(message)
            return 0
        
    def set_number(self, numero) -> None:
        self.position = numero
        l.log_file(109, f"{self.modbusI.address}, posizione: {self.position} ")