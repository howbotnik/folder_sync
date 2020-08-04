class Error:

    def __init__(self, message):
        self.message = message

    def to_string(self):
        return 'Error message: ' + str(self.message)