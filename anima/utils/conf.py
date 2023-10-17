from os import path as _path, chmod, chown  # noqa: F401
import subprocess
import json

def rchmod(path,permissions:bin):
    """
        Change file permissions
    """
    ...

class Conf:
    conf_path = _path.sep.join(__file__.split(_path.sep)[:-1])

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
    def manage_permissions(cls, path:str):
        try:
            err_code = [
                subprocess.run(["chmod","-R","444",path]),
                subprocess.run(["chmod","555",path]),
                subprocess.run(["chown","-R","nobody:nogroup",path])
            ]

            # chmod(path,0o444),
            # chmod(path,0o555),
            if err_code:
               raise RuntimeError(
                   f"Terjadi kesalahan saat mengubah izin file \
                   Subprocess output: {err_code}"
               )

        except PermissionError:
            raise PermissionError("Run this program with 'sudo'")


if __name__ == "__main__":
    Conf.make_read_only("./Folder/")