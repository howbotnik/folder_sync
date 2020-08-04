import pickle
import os

class File_Transactions:

    def __init__(self):
        self

    def create_file(self, contents, path):
        print('Entering create file with: ' + path)
        try:
            file = open(path, 'wb')
            pickle.dump(contents, file)
            file.close()
        except Exception as e:
            print('Error creating .folder_sync file')
            print(e)

    def read_file(self, path):
        try:
            infile = open(path, 'rb')
            object_to_return = pickle.load(infile)
            infile.close()
            return object_to_return
        except Exception as e:
            print('Error reading .folder_sync file')
            print(e)

    def does_file_exist(self, path):
        return os.path.exists(path)

    def delete_file(self, path):
        try:
            os.remove(path)
        except Exception as e:
            print('Error deleting old .folder_sync file')
            print(e)

