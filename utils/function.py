from os import path as _path, rename as _rename, listdir  # noqa: F401
from os.path import join as _join, exists  # noqa: F401


def rename(path:str):
    try:
        print("Bisa coy")
        print(listdir(path))
    except FileNotFoundError as e:
        raise FileNotFoundError(f"{e}\n\nFile tidak ditemukan!\nFile Not Found!")

    except PermissionError as e:
        raise PermissionError(
            f"{e}\nTidak dapat membuka folder, coba periksa izin dari folder tersebut \
            Can't open the folder, try checking the permissions of the folder"
        )

    print("End Function")

if __name__ == "__main__":
    debug = True

    rename("")