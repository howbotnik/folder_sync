import os
from folder import Folder
from file import File
from error import Error

class Crawler:
    file_sep = os.path.sep
    counter = 0

    error_list = []

    crawl_graphic = ['|', '/', '-', '\\', '/', '-', '\\']
    crawl_int = 0

    def __init__(self):
        self

    def crawl(self, folder, full_path):
        try:
            items = os.listdir(full_path)
        except Exception as e:
            items = []
            self.add_to_error_list(Error(e))

        for item in items:
            print("Found: " + item, end="                                          \r", flush=True)
            self.counter += 1
            if self.is_item_folder(item, full_path):
                #folder.add_item_to_folder(Folder(item, []).to_dict())
                folder.add_item_to_folder(self.crawl(Folder(item, []), full_path + self.file_sep + item).to_dict())
            else:
                try:
                    date_modified = os.path.getmtime(full_path + self.file_sep + item)
                except Exception as e:
                    self.add_to_error_list(Error(e))
                    date_modified = 1;
                folder.add_item_to_folder(File(item, date_modified).to_dict())
        return folder

    def is_item_folder(self, item, current_dir):
        return os.path.isdir(current_dir + self.file_sep + item)

    def reset_counter(self):
        self.counter = 0

    def get_counter(self):
        return self.counter

    def get_errors(self):
        return self.error_list

    def add_to_error_list(self, error):
        self.error_list.append(error)



