from os import path as _path, chmod, chown, walk  # noqa: F401
from pwd import getpwnam
from grp import getgrnam
import subprocess
import json

from .text import Messege
from .func import vprint

class Conf:

    default_conf = {
        "partition":None,
        "filesystem":"ext4",
        "destination":None,
    }
    verbose = False

    conf_path = _path.join(_path.sep.join(__file__.split(_path.sep)[:-2]),\
        "setting.json")

    user  = getpwnam("nobody").pw_uid
    group = getgrnam("nogroup").gr_gid

    @classmethod
    def read(cls) -> dict:
        if _path.exists(cls.conf_path):
            with open(cls.conf_path,"r") as f:
                out = json.load(f)
                if isinstance(out,dict):
                    return out
        
        with open(cls.conf_path,"w") as f:
            json.dump(cls.default_conf,f)
            return cls.default_conf
    
    @classmethod
    def write(cls,key:str,value:any) -> None:
        data = cls.read()
        data[key] = value
        with open(cls.conf_path,"w") as f:
            json.dump(data,f)



    @classmethod
    def manage_permission(cls,path:str):
        """
            Change file permissions
        """

        vprint("Change permission:",cls.verbose)

        if debug:
            print("-"*31)
        for root, dirs, files in walk(path):
            vprint(root[-29:].ljust(31), cls.verbose, end="")
            try:
                if not debug:
                    chmod(root,0o555)
                    chown(root,cls.user,cls.group)
                else:
                    ...
                vprint(Messege.ok,cls.verbose)
            except PermissionError:
                vprint(Messege.failed,cls.verbose)
                

            for i in files:
                dest = _path.join(root,i)
                vprint(dest[-29:].ljust(31), cls.verbose, end="")
                if not debug:
                    chmod(dest,0o444)
                    chown(dest,cls.user,cls.group)
                vprint(Messege.ok,cls.verbose)

    @classmethod
    def mount(cls,partition:str,dest:str,read_only:bool=False):

        if not _path.exists(partition) and not _path.exists(dest):
            print(Messege.FileFolderNotFound)
            return

        sh = ["mount",partition,dest]
        if read_only:
            sh.extend(["-o", "ro"])
        subprocess.run(sh,check=True)

    
    @classmethod
    def umount(cls,path:str):
        subprocess.run(["umount",path],check=True)


if __name__ == "__main__":
    path = "../test"
    debug = True
    
    # Conf.verbose = True
    print(
        Conf.read()
    )