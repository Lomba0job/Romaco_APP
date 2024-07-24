from API import modbus_strutture as st 
from API import modbus_unico as mb
from API import modbus

class Bilancia():
    
    def __init__(self, modbus_) -> None:
        self.modbusI: modbus.Instrument = modbus_
        self.position = None
        
    def start_set_position(self) -> str:
        print(f"Configurazione Bilancia {self.modbusI.address}")
        mb.set_accensione(self.modbusI)
        coil = 0
        while coil == 0:
            coil = mb.read_coil(self.modbusI)
            
        message = f"Bilancia N {self.modbusI.address} collegata ora"
        print(message)
        return message