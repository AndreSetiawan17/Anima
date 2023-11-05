from os import path as _path, listdir, remove, rename as _rename  # noqa: F401

from .conf import Conf
from .error import FolderRenamed, RenameFileError

debug = True

def rename_preview(path:str,ignore:list=None ,dump_to_file:bool=True):
    extension = ("mp4","mkv",  "avi","mov","wmv","flv","ogg","3gp","3p2")

    list_dir = sorted([
        # Memisah nama file dengan ekstensi file
        # Otakudesu.net_YPTSBT--01_360p.mp4 -> ['Otakudesu.net_YPTSBT--01_360p','mp4']
        [i.replace(i.split(".")[-1],"")[:-1], i.split(".")[-1]] \
        for i in listdir(path) \
        if i.split(".")[-1] in extension and (f"{i[0]}.{i[-1]}" not in ignore)
    ])

    if len(list_dir) < 1:
        raise FileNotFoundError

    ls_name = []
    for i,j in enumerate(list_dir):
        file_name = "Episode"

        if i < 9:
            file_name += "0"
        #             "Episode0" +    1     + "." + mp4"
        # ls_name.append(file_name + str(i+1) + "." + j[1])
        ls_name.append(f"{file_name}{i+1}.{j[1]}")
        
    ls_name = [i for i in zip([i[0] + "." + i[1] for i in list_dir],ls_name)]

    if ignore: ls_name = [i for i in ls_name if i[0] not in ignore]         # noqa: E701

    if dump_to_file:
        Conf.dump(_path.join(path,"rename.json"),ls_name)

    return ls_name


# @coba
def rename(
        path:str, folder_name:str=None, ignore:list=None,\
        use_rename_file:bool=False, ver:bool=True  
    ):
    """
        Return new path if folder_name is not None
    """

    # ['/home/user/Desktop/MyAnime/Special_720p_BD.mp4','other/anime/anggap_episode1.mp4] -> ['Special_720p_BD.mp4','anggap_episode1.mp4.mp4]
    if ignore:
        ignore = [i.split("/")[-1] for i in ignore]

    if use_rename_file and _path.exists(rename_path:=_path.join(path,"rename.json")):
        ls_name = Conf.load(rename_path)

        # Jika file yang ada pada rename.json setelah di deserialize tidak bertipe list akan membangkitkan error
        if not isinstance(ls_name,list): raise RenameFileError              # noqa: E701

        # Membangkitkan error jika status file pada folder sudah diganti nama
        if ls_name[-1]["renamed"]: raise FolderRenamed                      # noqa: E701

        # Menyaring file yang ada pada pengecualian
        if ignore: ls_name = [i for i in ls_name if i[0] not in ignore]     # noqa: E701

    else:
        ls_name = rename_preview(path,ignore,dump_to_file=True)
        print(f"Location: {path}")
        # Otakudesu.net_YPTSBT--01_360p.mp4 -> Episode01.mp4
        for before, after in ls_name:
            print(before, after,sep=" -> ")

        if ver:
            inp = input("Rename? [y/n]\n>>> ")
            if inp not in ["Y","y"] or inp is None or inp.split() == "":
                print("Not rename")
                exit()

    # Rename File
    for before, after in ls_name:
        if before not in ignore:
            _rename(_path.join(path,before),_path.join(path,after))

    if folder_name:
        new_path = _path.join("/".join(path.split("/")[:-1]), folder_name)
        
        # Rename folder name
        _rename(path,new_path)

        return new_path
    return path

def check(path:str):
    # Menagani masalah jika ketika melakukan program terhenti atau masalah lain yang menyebabkan program berhenti
    data = ls_name = None

    if _path.exists(data_path:=_path.join(path,"data.json")):
        data:dict = Conf.load(data_path)
    
    if _path.exists(ls_name_path:=_path.join(path,"rename.json")):
        ls_name:list = Conf.load(ls_name_path)
    
        # ls_name = [i for i in ls_name if i[0] in listdir(path)]    
    
    if isinstance(data,dict) and data["renamed"]:
        remove(ls_name_path)