from os import path as _path, chmod, chown, walk, getuid
from pwd import getpwnam, getpwall
from grp import getgrnam, getgrall
import subprocess
import json
import psutil

from utils.error import ConfigurationError

class Conf:
    def __init__(self, verbose:bool=False) -> None:
        self.__verbose    = False

        self.__list_user  = [i.pw_name for i in getpwall()]
        self.__list_group = [i.gr_name for i in getgrall()]
        
        self.__conf_default = {
            "partition":None,
            "destination":None,
            "user":"nobody",
            "group":"nogroup"
        }
        self.__uid = getuid()

        self.__conf_path  = _path.join(_path.sep.join(__file__.split(_path.sep)[:-2]),\
            "setting.json")

        if not (_path.exists(self.conf["partition"]) and _path.exists(self.conf["destination"])):
            raise ConfigurationError(f"{self.conf['partition']} or {self.conf['destination']} not found")

    def __getitem__(self,key):
        return self.conf[key]

    def __setitem__(self,key,value):
        self.conf = {key:value}

    def __verify(self):
        if self.__uid != 0:
            raise PermissionError("You need root privileges to run this code")

    # Mengatasi masalah jika user/group tidak ada
    @property
    def user(self) -> str:
        return getpwnam(self.conf.get("user",self.__conf_default["user"])).pw_gid

    @property
    def group(self) -> str:
        return getgrnam(self.conf.get("group",self.__conf_default["group"])).gr_gid

    @property
    def conf(self) -> dict:
        try:
            conf:dict = self.load(self.__conf_path)
            if not isinstance(conf,dict):
                return self.__conf_default
            return conf
        except json.decoder.JSONDecodeError:
            return self.__conf_default
        #!later{
        #   memeriksa ukuran file setting.json, jika lebih dari 1MB maka akan ditulis ulang
        # }

    @property
    def disk_free(self) -> float:
        """ Byte """
        return psutil.disk_usage(self.conf["destination"]).free

    @conf.setter
    def conf(self, dict:dict):
        conf = self.conf
        conf.update(dict)     
        self.dump(self.__conf_path,conf)

    @user.setter
    def user(self, user:str):
        self.conf = {"user":user}

    @group.setter
    def group(self, group:str):
        self.conf = {"group":group}

    @staticmethod
    def load(path:str) -> any:
        try:
            with open(path,"r") as f:
                return json.load(f)
        except FileNotFoundError:
            ...
        except PermissionError:
            ...

    @staticmethod
    def dump(path:str, data:any) -> None:
        try:
            with open(path,"w") as f:
                json.dump(data,f)
        except PermissionError:
            ...
        #!later{
        #   mengatasi masalah PermissionError dan mungkin ruang penuh
        # }

    @staticmethod
    def extension():
        return ("mp4","mkv",  "avi","mov","wmv","flv","ogg","3gp","3p2")

    def partition_mountpoint(self,directory:str=None,device:str=None) -> any:
        """
                Jika kedua argument diisi, program akan mencocokkan antara dimana mount point dari device dan jika sama dengan directory akan mengembalikan nilai True.\n
                Jika mengisi salah satunya maka nilai yang akan dikembalikan adalah nilai dari argument satunya \n
            Misal, directory='/mnt', maka fungsi akan mengembalikan nilai str yang bertuliskan partisi yang dimount pada lokasi tersebut
        """
        for partition in psutil.disk_partitions(True):
            if (device and directory) and \
                ((partition.mountpoint == directory) and (partition.device == device)):
                return True

            elif directory and partition.mountpoint == directory:
                return partition.device

            elif device and partition.device == device:
                return partition.mountpoint

        return False
        # partitions = [
        #     [i.device, i.mountpoint] 
        #     for i in psutil.disk_partitions(True)
        #     # if i.device.split("/")[-1][0:2] == self.conf["partition"].split("/")[-1][0:2]
        #     if i.device.startswith("/dev")
        # ]
        # partition  = [i[0] for i in partitions]
        # mountpoint = [i[1] for i in partitions]

    def folder_size(cls,path:str) -> float:
        """ Byte """
        print(path)
        size = 0
        for dirpath, dirnames, filenames in walk(path):
            for filename in filenames:
                size += _path.getsize(_path.join(dirpath, filename))
        return size

    def restrict_access(self,path:str):    
        if not _path.exists(path):
            raise FileNotFoundError(f"{path} not found")
        
        for root, dirs, files in walk(path):
            chmod(root,0o555)
            chown(root,self.user,self.group)

            for i in files:
                dest = _path.join(root,i)
                print(dest)
                chmod(dest,0o444)
                chown(dest,self.user,self.group)

    def sync(self,src:str,remove:bool=False):
        command = ["rsync"]
        
        command.extend(["-avh","--progress"]) if self.__verbose else command.append("-a")
        ## Penyederhanaan dari code diatas:
        # if self.__verbose:
        #     command.extend(["-avh","--progress"])
        # else:
        #     command.append("-a")

        if remove:
            command.append("--remove-source-files")

        # Sumber dan Tujuan
        # Menghapus / pada bagian belakang source agar rsync menyalin bersama foldernya,  bukan file yang ada di dalam folder saja
        command.extend([src.rstrip("/"),self.conf["destination"]])

        subprocess.run(command,check=True)

        # if remove:
        #     rmdir(src)

    def mount(self,read_only:bool=False):
        self.__verify()        

        command = ["mount",self.conf["partition"],self.conf["destination"]]

        if read_only:
            command.extend(["-o","ro"])
        
        subprocess.run(command,check=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def umount(self,path:str=None,device:str=None):
        self.__verify()
        command = ["umount"]
        
        if path:
            command.extend([path])
        elif device:
            command.extend([self.partition_mountpoint(device=device)])
        else:
            command.extend([self.conf["destination"]])

        try:
            subprocess.run(command,check=True)
        except Exception as e:
            raise OSError(f"Can't umount, close all programs accessing the partition.\n{e}")