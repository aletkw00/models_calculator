import os.path as path
import json

"""
parte per il logging
"""

class Log:
    def __init__(self, file):
        self.file = file
        self.dict = {}

    def legge_crea(self):
        """
        Funzione che legge il log o lo crea
        """
        if not path.exists(self.file):
            self.dict = {"riga": 0}

        else:
            with open(self.file, 'r') as f:
                self.dict = json.load(f)
                if "ultimo_errore" in self.dict.keys():
                    self.dict.pop("ultimo_errore")

    def salva(self):
        """
        Funzione che salva il log
        """
        json_object = json.dumps(self.dict, indent=4)
        with open(self.file, 'w') as f:
            f.write(json_object)

    def incrementa_riga(self):
        """
        Funzione che incrementa il contatore delle righe
        """
        self.dict.update({"riga": (self.dict.get("riga") + 1)})
        Log.salva(self)

    def errore(self, testo):
        self.dict.update({"ultimo_errore": testo})
        Log.salva(self)

    def get_riga(self):
        return int(self.dict.get("riga"))

    def set_riga(self, numero: int):
        self.dict.update({"riga": numero})
        Log.salva(self)