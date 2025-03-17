import os
from pathlib import Path

class Cacher():



    def __init__(self):

        # 1: Create the cache file if it doesn't already exist
        message_cache = "message_cache"
        recorded_ids_txt = "recorded_ids.txt"
        cache_folder_path = Path(message_cache)
        cache_file_path = Path(message_cache).joinpath(recorded_ids_txt)

        if not os.path.exists(cache_folder_path):
            os.mkdir(cache_folder_path)
        if not os.path.exists(cache_file_path):
            id_cache_file = os.open(cache_file_path, os.O_CREAT)

        # 2: Have the filepath name ready for other methods
        self.filepath = "message_cache/recorded_ids.txt"


    def read_ids(self):

        try:
            read_file = open(self.filepath, "r")
            ids_read = read_file.read()
            cached_ids = set(ids_read.split("\n"))

            read_file.close()
            return cached_ids
        
        except FileNotFoundError as error:
            print(f"The file was deleted mid-execution: {error}")
            return None



    def add_ids(self, id_list: list[str]):

        try:
            append_file = open(self.filepath, "a")

            id_string = "\n" + "\n".join(id_list)
            append_file.write(id_string)

            append_file.close()

        except FileNotFoundError as error:
            print(f"The file was deleted mid-execution: {error}")
