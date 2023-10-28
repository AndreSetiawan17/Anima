from os import path as _path, chmod, chown, walk
from pwd import getpwnam
from grp import getgrnam
import subprocess
import json
import psutil

class Conf:
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

        raise RuntimeError("Konfigurasi tidak tersedia")
        
    @classmethod
    def write(cls,key:str,value:any) -> None:
        data = cls.read()
        data[key] = value
        with open(cls.conf_path,"w") as f:
            json.dump(data,f)

    @classmethod
    def manage_permission(cls,path:str):
        for root, dirs, files in walk(path):
            chmod(root,0o555)
            chown(root,cls.user,cls.group)

            for i in files:
                dest = _path.join(root,i)
                chmod(dest,0o444)
                chown(dest,cls.user,cls.group)

    @classmethod
    def mount(cls,read_only:bool=False):
        sh = ["mount",conf["partition"],conf["destination"]]
        if read_only:
            sh.extend(["-o", "ro"])

        subprocess.run(sh,check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @classmethod
    def umount(cls,path:str=None):
        if cls.partition_mountpoint(path) is not None or cls.partition_mountpoint(conf["destination"]) is not None:
            ...

        if path:
            subprocess.run(["umount","-l",path],check=True)
        else:
            subprocess.run(["umount","-l",conf["destination"]],check=True)
    
    @classmethod
    def disk_free(cls) -> int:
        """ Byte """
        return psutil.disk_usage(conf["destination"]).free
    
    @classmethod
    def folder_size(cls,path:str) -> float:
        total = 0
        for dirpath, dirnames, filenames in walk(path):
            for filename in filenames:
                total += _path.getsize(_path.join(dirpath, filename))
        return total
    
    @classmethod
    def partition_mountpoint(cls,directory:str=None,device:str=None) -> str:
        for partition in psutil.disk_partitions(True):    

            if directory and partition.mountpoint == directory:
                return partition.device
            
            elif device and partition.device == device:
                return partition.mountpoint
            
            # elif (directory and device):
            #     ...

    @classmethod
    def sync(cls,src:str,remove:bool=True,verbose:bool=False):

        sh = ["rsync"]
        if verbose:
            sh.append("-avh --progress")
        else:
            sh.append("-a")
        
        if remove:
            sh.append("--remove-source-files")

        sh.extend([src,conf["destination"]])
        subprocess.run(sh,check=True)
    
debug = False
conf = Conf.read()