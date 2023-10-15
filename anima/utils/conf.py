import subprocess
import json
import os


class Conf:
    conf_path = os.path.sep.join(__file__.split(os.path.sep)[:-1])

    default_conf = {
        "dest":None, # Lokasi dari file yang akan disimpan
        
    }

    @classmethod
    def read(cls):
        with open(cls.conf_path,"r") as f:
            return json.load(f)
    
    @classmethod
    def write(cls, data):
        with open(cls.conf_path,"w") as f:
            json.dump(data,f)
    
    @classmethod
    def make_read_only(cls, path):
        try:
            err_code = subprocess.run(["chmod","a-wx","*"])
            if err_code:
               raise RuntimeError(
                   f"Terjadi kesalahan saat mengubah izin file \
                   Subprocess output: {err_code}"
               )

        except PermissionError:
            raise PermissionError("Run this program with 'sudo'")