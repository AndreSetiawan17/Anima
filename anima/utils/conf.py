from os import listdir, path as _path, chmod, chown, walk  # noqa: F401
from pwd import getpwnam
from grp import getgrnam
import subprocess
import json

from text import Text

def vprint(text:str,verbose:bool,sep:any=" ",end:any="\n"):
    """
        Print if verbose
    """
    if verbose:
        print(text,sep=sep,end=end)

class Conf:

    default_conf = {
        "dest":None, # Lokasi dari file yang akan disimpan  
    }
    verbose = False

    conf_path = _path.sep.join(__file__.split(_path.sep)[:-1])
    user  = getpwnam("nobody").pw_uid
    group = getgrnam("nogroup").gr_gid


    @classmethod
    def read(cls):
        with open(cls.conf_path,"r") as f:
            return json.load(f)
    
    @classmethod
    def write(cls, data):
        with open(cls.conf_path,"w") as f:
            json.dump(data,f)

    @classmethod
    def rchmod(cls,path:str):
        """
            Change file permissions
        """

        for root, dirs, files in walk(path):

            vprint(f"Change permission: --{root[-10:]}".ljust(31),end="")            
            try:
                chmod(root,0o555)
                chown(root,cls.user,cls.group)
                vprint(f"[{Text.ok}]",cls.verbose)
            except PermissionError:
                ...

            for i in files:
                chmod(_path.join(root,i),0o444)
                chown(_path.join(root,i),cls.user,cls.group)
    
    # @classmethod
    # def manage_permissions(cls, path:str):
    #     try:
    #         err_code = [
    #             subprocess.run(["chmod","-R","444",path]),
    #             subprocess.run(["chmod","555",path]),
    #             subprocess.run(["chown","-R","nobody:nogroup",path])
    #         ]

    #         # chmod(path,0o444),
    #         # chmod(path,0o555),
    #         if err_code:
    #            raise RuntimeError(
    #                f"Terjadi kesalahan saat mengubah izin file \
    #                Subprocess output: {err_code}"
    #            )

    #     except PermissionError:
    #         raise PermissionError("Run this program with 'sudo'")


if __name__ == "__main__":
    Conf.rchmod("./test")