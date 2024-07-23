from API import modbus_strutture as st 
from API import modbus_unico as mb


class Bilancia():
    
    def __init__(self, modbus) -> None:
        self.modbus = modbus
        self.position = None
        