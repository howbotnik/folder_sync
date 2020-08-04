import os
from folder import Folder
from crawler import Crawler
import sys
from differences import Differences
import threading
import time
from file_transactions import File_Transactions
import ctypes


def main():
    print("Entering main")
    print("Is admin: " + str(is_admin()))
    if is_admin():
        file_transactions = File_Transactions()
        error_list = []

        start_time = time.time()
        file_sep = os.path.sep

        src_string = sys.argv[1]
        dest_string = sys.argv[2]

        src_folder = Folder(src_string, [])

        dest_folder = Folder(dest_string, [])

        crawler = Crawler()
        print('Scanning source directory... please wait.')
        src = crawler.crawl(src_folder, src_string)
        src_crawl_counter = crawler.get_counter()
        file_transactions.create_file(src, src.name + '//' + '.folder_sync.lib')
        error_list += crawler.get_errors()

        crawler.reset_counter()

        # DOES DESTINATION NEED TO BE CRAWLED? Checking for cached version
        if file_transactions.does_file_exist(dest_string + '//' + '.folder_sync.lib'):
            print('Destination has been scanned before, using cached version.')
            dest = file_transactions.read_file(dest_string + '//' + '.folder_sync.lib')
        else:
            print('Scanning destination directory... please wait.')
            dest = crawler.crawl(dest_folder, dest_string)

        print('Starting sync...')
        differences = Differences()
        t = threading.Thread(target = start_differences, name = 'update_dest', args = (differences, src.items, dest.items, src.name, dest.name))
        t.start()

        copied = 0
        while t.is_alive():
            time.sleep(0.5)
            end_time = time.time()
            elapsed_time = end_time - start_time
            time_array = format_seconds_to_hhmmss(elapsed_time)
            time_string = str(time_array)
            while not differences.q.empty():
                copied = differences.q.get()
            print(str(copied) + ' // ' + str(src_crawl_counter) + ': ' + str(
                round((copied / src_crawl_counter) * 100, 1)) + '% complete. Elapsed time: ' + time_string)
        print('Mirror Syncronisation complete!')

        ## send new cached version to dest folder
        print('Creating cache in dest folder')
        if file_transactions.does_file_exist(dest_string + file_sep + '.folder_sync.lib'):
            file_transactions.delete_file(dest_string + '//' + '.folder_sync.lib')

        src.name = dest.name
        file_transactions.create_file(src, src.name + '\\' + '.folder_sync.lib')

        print('Errors when copying/reading files: ' + str(len(error_list)))
        error_list += differences.get_errors()
        #for error in error_list:
        #    print(error.to_string())
        print('Total number changed: ' + str(differences.total_num_transferred))
        print('Total size changed: ' + str(differences.total_size_transferred) + ' bytes')

        close_program = ''
        while close_program != 'y':
            close_program = input('Enter y to close program.')

    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def start_differences(differences, src_items, dest_items, src_name, dest_name):
    differences.get_differences(src_items, dest_items, src_name, dest_name)
    differences.q.empty()
    return differences.get_count()

def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    main()