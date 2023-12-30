from time import time
import subprocess
import psutil
import json
import pwd
import grp
import os

# import hashlib

class ConfigurationError(Exception): ...

class Conf:
    def __init__(self, verbose:bool=False) -> None:
        self.__verbose    = verbose

        self.__list_user  = [i.pw_name for i in pwd.getpwall()]
        self.__list_group = [i.gr_name for i in grp.getgrall()]
        self.__path       = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.__conf_path  = os.path.join(self.__path,"setting.json")
        self.__uid        = os.getuid()
        self.__default    = {
            "partition":None,
            "location":None,
            "user":pwd.getpwuid(self.__uid).pw_name,
            "group":grp.getgrgid(self.__uid).gr_name
        }

    # def __getitem__(self,key):
    #     return self.conf[key]

    # def __setitem__(self,key,value):
    #     self.conf = {key:value}

    def __verify(self):
        if self.__uid != 0:
            raise PermissionError("You need root privileges to run this code")

    @property
    def conf(self) -> dict:
        if not os.path.exists(self.__conf_path):
            print("[Warning] Configuration not found!.\nConfigure with the command 'anima config'")
            return self.__default
        return self.load(self.__conf_path)
        # json.JSONDecodeError

    @property
    def free(self) -> float:
        return psutil.disk_usage(self.conf["location"]).free

    @property
    def extension(self):
        return ("mp4","mkv","webp")

    @property
    def user(self) -> str:
        user = self.conf["user"]
        if user not in self.__list_user:
            print(f"Couldn't find user {user}, used user {self.__default['user']} as default")

        return pwd.getpwnam(self.conf.get(
            "user",self.__default["user"]
        )).pw_gid

    @property
    def group(self) -> str:
        group = self.conf["group"]
        if group not in self.__list_group:
            print(f"Couldn't find user {group}, used group {self.__default['group']} as default")

        return grp.getgrnam(self.conf.get(
            "group",self.__default["group"]
        )).gr_gid

    @property
    def partition(self) -> str:
        part = self.conf["partition"]
        if not os.path.exists(part):
            raise ConfigurationError(f"{part} not found")
        return part

    @property
    def location(self) -> str:
        loc = self.conf["location"]
        if not os.path.exists(loc):
            raise ConfigurationError(f"{loc} not found")
        return loc

    @conf.setter
    def conf(self, data:dict):
        c = self.conf
        c.update(data)
        self.dump(self.__conf_path,c)

    @user.setter
    def user(self, user:str):
        if user not in self.__list_user:
            raise OSError(f"{user} not found")
        self.conf = {"user":user}

    @group.setter
    def group(self, group:str):
        if group not in self.__list_group:
            raise OSError(f"{group} not found")
        self.conf = {"group":group}

    @partition.setter
    def partition(self,path:str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Can't find {path}")
        self.conf = {"partition":path}

    @location.setter
    def location(self,path:str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Can't find {path}")
        self.conf = {"location":path}

    @staticmethod
    def load(path:str) -> any:
        with open(path,"r") as f:
            return json.load(f)
    # PermissionError
    # FileNotFoundError
    # json.JSONDecodeError
    @staticmethod
    def dump(path:str, data:any) -> None:
        with open(path,"w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def size(path:str) -> float:
        """ Byte """
        size = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                size += os.path.getsize(os.path.join(dirpath, filename))
        return size


    def edit(self, data:any):
        path = os.path.join(self.__path,"temp",f"{time()}.json")
        self.dump(path,data)
        subprocess.run(["nano",path])

        try:
            return self.load(path)
        except json.decoder.JSONDecodeError:
            print("[Warning] Invalid configuration, restoring to default...")
            return data
        finally:
            os.remove(path)

    def partition_mountpoint(self,directory:str=None,partition:str=None) -> any:
        """
                Jika kedua argument tidak diisi, program akan mencocokkan antara dimana mount point dari partition dan jika sama dengan directory akan mengembalikan nilai True.\n
                Jika mengisi salah satunya maka nilai yang akan dikembalikan adalah nilai dari argument satunya \n
            Misal, directory='/mnt', maka fungsi akan mengembalikan nilai str yang bertuliskan partisi yang dimount pada lokasi tersebut
        """

        for part in psutil.disk_partitions(True):
            if (partition is None and directory is None) and \
                ((part.mountpoint == self.location) and (part.device == self.partition)):
                return True

            elif directory and part.mountpoint == directory:
                return part.device

            elif partition and part.device == partition:
                return part.mountpoint

        return False

    def restrict_access(self,path:str):    
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")

        for root, dirs, files in os.walk(path):
            os.chmod(root,0o555)
            os.chown(root,self.user,self.group)

            for i in files:
                dest = os.path.join(root,i)
                os.chmod(dest,0o444)
                os.chown(dest,self.user,self.group)

    def sync(self,source:str,remove:bool=False):
        command = ["rsync"]

        command.extend(["-avh","--progress"]) if self.__verbose else command.append("-a")
        command.append("--removce-source-files") if remove else None

        # Menghapus '/' pada bagian belakang source agar rsync menyalin bersama foldernya,  bukan file yang ada di dalam folder saja
        command.extend([source.rstrip("/"),self.location])

        subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def mount(self,read_only:bool=False):
        self.__verify()
        command = ["mount", self.partition, self.location]

        command.extend(["-o","ro"]) if read_only else None
        
        subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def umount(self,path:str=None):
        self.__verify()
        command = ["umount"]

        command.append(path) if path else command.append(self.location)

        subprocess.run(command,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    def rename(self,path:str,ignore:list=[],yes:bool=False) -> None:
        if not os.path.exists(path) and not os.path.isdir(path):
            print(f"Skipping '{path}' because it wasn't found or it's not a folder")

        print(f"Path: {path}")

        listdir   = [
            i for i in sorted(os.listdir(path)) \
            if i.split(".")[-1] in self.extension and i not in ignore
        ]
        after     = [
            f"Episode{i+1:02d}.{extension}"
            for i,extension in enumerate(
                [filename.split(".")[-1] for filename in listdir]
            ) if True is True
        ]
        filename  = {k:v for k,v in zip(listdir,after)}

        while not yes:
            for before,after in filename.items():
                print(before,after,sep=" -> ")

            print("Rename? [y/n] or [e] for edit.")
            try:
                inp = input(">>> ").lower()
            except KeyboardInterrupt:
                inp = False

            match inp:
                case "y":
                    break
                case "e":
                    filename = self.edit(filename)
                case _:
                    print("Skipping...")
                    return

        for before,after in filename.items():
            os.rename(
                os.path.join(path,before),
                os.path.join(path,after)
            )