import os
import struct
from API import LOG as l, funzioni as f

class SettingsManager:
    def __init__(self) -> None:
        self.file = f.get_bin()
        self.lettura = False
        self.auto_tara = False
        self.peso = 20
        self.read_file()
    
    def read_file(self):
        # Check if the file exists
        if not os.path.exists(self.file):
            print(f"File {self.file} does not exist. Creating with default values.")
            self.write_file()  # Create the file with default values
        else:
            try:
                with open(self.file, 'rb') as f:
                    data = f.read()
                    if len(data) == 10:  # We expect exactly 10 bytes (2 booleans + 1 integer)
                        self.lettura, self.auto_tara, self.peso = struct.unpack('??i', data)
                        l.log_file(19)
                    else:
                        l.log_file(423)
                        self.lettura, self.auto_tara, self.peso = False, False, 20
                        self.write_file()
            except Exception as e:
                l.log_file(424, f" {e}")
                self.lettura, self.auto_tara, self.peso = False, False, 20
                self.write_file()
    
    def set_lettura(self, state: bool, peso: int):
        self.lettura = state
        self.peso = peso
        self.write_file()
    
    def set_autoTara(self, state: bool):
        self.auto_tara = state
        self.write_file()
    
    def get_lettura(self) -> bool:
        return self.lettura
    
    def get_lettura_val(self) -> int:
        return self.peso
    
    def get_autotare(self) -> bool:
        return self.auto_tara
    
    def write_file(self):
        try:
            with open(self.file, 'wb') as f:
                data = struct.pack('??i', self.lettura, self.auto_tara, self.peso)
                f.write(data)
                l.log_file(20)
        except Exception as e:
            l.log_file(425, f" {e}")