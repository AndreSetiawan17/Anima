from os import path as _path

"""
    Loging menggunakan decorator

    Mencatat semua hal yang akan dilakukan dan statusnya setelah dijalankan
    lalu melakukan tindakan tambahan jika ada yang gagal

"""

class Log:
    log_path = _path.join(
        _path.sep.join(__file__.split(_path.sep)[:-2]),
        "log.json"
    )

    @property
    def log(cls):
        try:
            with open(cls.log_path, "r") as f:
                return f.readlines()
        except PermissionError:
            ...
        


if __name__ == "__main__":
    print(Log.log_path)