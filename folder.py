class Folder:

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def add_item_to_folder(self, item):
        self.items.append(item)

    def get_item_list(self):
        return self.items

    def get_name(self):
        return self.name

    def to_string(self):
        return 'Folder Object: ' + self.get_name() + ' ' + str(self.get_item_list())

    def to_dict(self):
        return {
            'name': self.get_name(),
            'items': self.get_item_list()
        }
