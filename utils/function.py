from os import path as _path, rename as _rename, listdir  # noqa: F401

def rename(path:str, ver:bool = True):
    ekstensi = ("mp4","mkv",  "avi","mov","wmv","flv","ogg","3gp","3p2")

    try:
        list_dir = sorted([
            # out -> ['Otakudesu.net_YPTSBT--01_360', 'mp4']
            [i.replace(i.split(".")[-1],"")[:-1], i.split(".")[-1]] \
            for i in listdir(path) \
            if i.split(".")[-1] in ekstensi
        ])

        ls_name = []
        for i,j in enumerate(list_dir):
            file_name = "Episode"
            if i < 9:
                file_name += "0"
            #             "Episode0" +    1     + "." + mp4"
            ls_name.append(file_name + str(i+1) + "." + j[1])
            
        ls_name = [i for i in zip([i[0] + "." + i[1] for i in list_dir],ls_name)]
        print(f"Lokasi: {path} \n")

        # Otakudesu.net_YPTSBT--01_360.mp4 -> Episode01.mp4
        for before, after in ls_name:
            print(before, after,sep=" -> ")

        if ver:
            inp = input("Rename? [yes/no]\n>>> ")
            print(type(inp),inp)
            if inp in ["Yes","yes","No","no"]:
                return

        # Rename File
        for i,j in ls_name:
            _rename(_path.join(path,i),_path.join(path,j))

    except FileNotFoundError as e:
        raise FileNotFoundError(f"{e}\n\nFile tidak ditemukan!\nFile Not Found!")

    except PermissionError as e:
        raise PermissionError(
            f"{e}\nTidak dapat membuka folder, coba periksa izin dari folder tersebut \
            Can't open the folder, try checking the permissions of the folder"
        )


if __name__ == "__main__":
    ...