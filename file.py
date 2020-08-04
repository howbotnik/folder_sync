class File:

    name = ''
    date_modified = 0

    def __init__(self, name, date_modified):
        self.name = name
        self.date_modified = date_modified

    def get_name(self):
        return self.name

    def get_date_modified(self):
        return self.date_modified

    def to_string(self):
        return 'File Object: ' + self.get_name() + ' ' + self.get_date_modified()

    def to_dict(self):
        return {
            'name': self.get_name(),
            'date_modified': self.get_date_modified()
        }