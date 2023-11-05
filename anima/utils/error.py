from termcolor import colored as c


class ConfigurationError(Exception): ...
class NotEnoughSpace(Exception): ...
class RenameFileError(Exception): ...
class FolderRenamed(Exception): ...

class ID:
    permission_error = f"{c('Akses ditolak','red',attrs=['bold'])}\nCoba beri pengguna akses ke file atau jalankan perintah dengan {c('sudo',attrs=['bold'])}"
    configuration_error = f"Terjadi kesalahan pada {c('file konfigurasi','red',attrs=['bold'])}\nAtur ulang kofigurasi dengan menggunakan command {c('anima config',attrs=['bold'])}"
    not_enough_space = f"partisi sudah {c('penuh','red',attrs=['bold'])}"

class EN:
    permission_error:str
    configuration_error:str

def coba(func):    
    def wrapper(*args,**kwargs):
        try:
            out = func(*args,**kwargs)
            return out
    
        except ConfigurationError:
            match lang:
                case "id":
                    print(ID.configuration_error)
                case "en":
                    print(EN.configuration_error)
            
        except PermissionError:
            match lang:
                case "id":
                    print(ID.permission_error)
                case "en":
                    print(EN.permission_error)

        except FileNotFoundError:
            match lang:
                case "id":
                    ...
                case "en":
                    ...

        except NotEnoughSpace:
            match lang:
                case "id":
                    ...
                case "en":
                    ...

    return wrapper

lang = 'id'

@coba
def main():
    raise ConfigurationError

if __name__ == "__main__":
    main()