from os import path as _path, chmod, chown, walk  # noqa: F401
from pwd import getpwnam
from grp import getgrnam
import subprocess
import json

from text import Text, Messege
from func import vprint

class Conf:

    default_conf = {
        "partition":None,
        "destination":None,
    }
    verbose = False

    conf_path = _path.sep.join(__file__.split(_path.sep)[:-1])
    user  = getpwnam("nobody").pw_uid
    group = getgrnam("nogroup").gr_gid


    @classmethod
    def read(cls) -> any:
        with open(cls.conf_path,"r") as f:
            return json.load(f)

    @classmethod
    def write(cls,data:any) -> None:
        with open(cls.conf_path,"w") as f:
            json.dump(data,f)

    @classmethod
    def manage_permission(cls,path:str):
        """
            Change file permissions
        """

        vprint("Change permission:",cls.verbose)

        for root, dirs, files in walk(path):
            vprint(root[-29:].ljust(31), cls.verbose, end="")
            # @coba
            # chmod(root,0o555)
            # @coba
            # chown(root,cls.user,cls.group)
            vprint(Text.ok,cls.verbose)

            for i in files:
                dest = _path.join(root,i)
                vprint(dest[-29:].ljust(31), cls.verbose, end="")
                # @coba
                # chmod(dest,0o444)
                # @coba
                # chown(dest,cls.user,cls.group)
                vprint(Text.ok,cls.verbose)

    @classmethod
    def mount(cls,partition:str,dest:str,read_only:bool=False):

        if not _path.exists(partition) and not _path.exists(dest):
            return Messege.FileFolderNotFound

        sh = ["mount",partition,dest]
        if read_only:
            sh.extend(["-o", "ro"])
        subprocess.run(sh,check=True)

    
    @classmethod
    def umount(cls,path:str):
        subprocess.run(["umount",path],check=True)


if __name__ == "__main__":
    Conf.verbose = True
    Conf.manage_permission("../test")