class Transaction:
    destination_path = ''
    source_path = ''
    duty = ''

    def __init__(self, source_path, destination_path, duty):
        self.source_path = source_path
        self.destination_path = destination_path
        self.duty = duty

    def get_duty(self):
        return self.duty

    def get_source_path(self):
        return self.source_path

    def get_destination_path(self):
        return self.destination_path


