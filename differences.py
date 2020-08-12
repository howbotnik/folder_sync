import os
import shutil
import queue
from error import Error
from transaction import Transaction

class Differences:
    list_of_transactions = []

    q = queue.Queue()
    error_list = []
    total_size_transferred = 0
    total_num_transferred = 0

    def __init__(self):
        self

    file_sep = os.path.sep
    count = 0

    def get_differences(self, list1, list2, full_src_path, full_dest_path):
        list2_names = self.get_names_from_item_array(list2)
        list1_names = self.get_names_from_item_array(list1)

        for item in list1:
            self.count += 1
            self.q.put(self.count)
            if 'items' in item:
                if item['name'] in list2_names:
                    list2_names.remove(item['name'])
                    self.get_differences(item['items'], self.get_list_from_item_name(list2, item['name']), full_src_path + self.file_sep + item['name'],
                                    full_dest_path + self.file_sep + item['name'])
                else:
                    self.make_folder(item['name'], full_dest_path)
                    self.get_differences(item['items'], [], full_src_path + self.file_sep + item['name'], full_dest_path + self.file_sep + item['name'])
            else:
                if item['name'] in list2_names:
                    item_b = self.get_item_from_filename_ref(list2, item['name'])
                    item_b = self.get_item_from_filename_ref(list2, item['name'])
                    if item_b['name'] == item['name'] and item['date_modified'] > item_b['date_modified']:
                        self.copy_file(item['name'], full_src_path, full_dest_path, 1)
                        list2_names.remove(item['name'])
                else:
                    self.copy_file(item['name'], full_src_path, full_dest_path, 1)

        self.delete_destination_files(list1_names, list2_names, full_dest_path)



    def delete_destination_files(self, list1_names, list2_names, full_dest_path):
        for item in list2_names:
            if item not in list1_names:
                print('Deleting file: ' + str(item))
                self.delete_item(item, full_dest_path)

    def get_names_from_item_array(self, list):
        str_list = []
        for item in list:
            str_list.append(item['name'])
        return str_list

    def make_folder(self, filename, path):
        try:
            os.mkdir(path + self.file_sep + filename)
        except Exception as e:
            self.add_to_error_list(Error(e))


    def delete_item(self, filename, path):
        if os.path.isdir(path + self.file_sep + filename):
            try:
                shutil.rmtree(path + self.file_sep + filename)
            except Exception as e:
                self.add_to_error_list(Error(e))
        else:
            try:
                os.remove(path + self.file_sep + filename)
            except Exception as e:
                self.add_to_error_list(Error(e))


    def copy_file(self, file_name, src_path, dest_path, attempt):
        if file_name == '.folder_sync.lib':
            return
        try:
            print('Copying: ' + src_path + '//' + file_name)
            shutil.copyfile(src_path + self.file_sep + file_name, dest_path + self.file_sep + file_name)
            self.total_num_transferred += 1
            self.total_size_transferred += os.path.getsize(src_path + self.file_sep + file_name)
        except Exception as e:
            #if e.args[0] == 'Errno 13' and attempt <= 5:
            #    print('error copying file, trying again...')
            #    time.sleep(5)
            #    self.copy_file(file_name, src_path, dest_path, attempt + 1)
            self.add_to_error_list(Error(e))

            
    def get_list_from_item_name(self, list, item_name):
        list_to_return = []
        for item in list:
            if item_name == item['name']:
                try:
                    list_to_return = item['items']
                except Exception as e:
                    self.add_to_error_list(Error(e))
                break
        return list_to_return

    def get_item_from_filename_ref(self, list, reference):
        for item in list:
            if item['name'] == reference:
                return item

    def get_count(self):
        return self.count

    def get_errors(self):
        return self.error_list

    def add_to_error_list(self, error):
        self.error_list.append(error)
