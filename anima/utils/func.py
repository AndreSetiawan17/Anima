from os import path as _path, rename as _rename, listdir
import subprocess  # noqa: F401

debug = True

def rename(path:str, folder_name:str=None, ver:bool=True):
    """
        Return new path
    """
    ekstensi = ("mp4","mkv",  "avi","mov","wmv","flv","ogg","3gp","3p2")

    list_dir = sorted([
        [i.replace(i.split(".")[-1],"")[:-1], i.split(".")[-1]] \
        for i in listdir(path) \
        if i.split(".")[-1] in ekstensi
    ])

    if len(list_dir) < 1:
        print("File not Found")
        exit()

    ls_name = []
    for i,j in enumerate(list_dir):
        file_name = "Episode"
        if i < 9:
            file_name += "0"
        #             "Episode0" +    1     + "." + mp4"
        ls_name.append(file_name + str(i+1) + "." + j[1])
        
    ls_name = [i for i in zip([i[0] + "." + i[1] for i in list_dir],ls_name)]
    print(f"Location: {path}")

    # Otakudesu.net_YPTSBT--01_360.mp4 -> Episode01.mp4
    for before, after in ls_name:
        print(before, after,sep=" -> ")

    if ver:
        inp = input("Rename? [y/n]\n>>> ")
        if inp not in ["Y","y"] or inp is None or inp.split() == "":
            if debug:
                print("Not rename")
            exit()

    # Rename File
    for i,j in ls_name:
        _rename(_path.join(path,i),_path.join(path,j))
    
    if folder_name:
        subprocess.run([
            "mv", path, _path.join(
                "/".join(path.split("/")[:-2]), folder_name
            )
        ])
        return _path.join("/".join(path.split("/")[:-2]), folder_name)
    return path

def vprint(text:str,verbose:bool,sep:any=" ",end:any="\n"):
    """
        Print if verbose
    """
    if verbose:
        print(text,sep=sep,end=end)

if __name__ == "__main__":
    ...