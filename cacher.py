import os
from pathlib import Path

class Cacher():



    def __init__(self):

        message_cache = "message_cache"
        recorded_ids_txt = "recorded_ids.txt"
        cache_folder_path = Path(message_cache)
        cache_file_path = Path(message_cache).joinpath(recorded_ids_txt)

        if not os.path.exists(cache_folder_path):
            os.mkdir(cache_folder_path)

        self.id_cache_file = os.open(cache_file_path, os.O_CREAT | os.O_RDWR)



    def write(self, string: str):
        os.write(self.id_cache_file, string.encode('ASCII'))



    def close(self):
        os.close(self.id_cache_file)