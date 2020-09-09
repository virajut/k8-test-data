import magic


class ValidateFile(object):

    def __init__(self, filename, file):
        self.filename = filename
        self.file = file

    def validate_file_type(self):
        file_mime_type = magic.from_file(self.file, mime=True)
        file_ext = self.filename.split('.').pop()

        if self.is_valid_mime_type(file_mime_type):
            return True
        return False

    @staticmethod
    def is_valid_mime_type(file_mime_type):
        valid_mime_types = ['video/quicktime', 'text/plain']
        for i in range(0, len(valid_mime_types)):
            if valid_mime_types[i].lower() == file_mime_type.lower():
                return True

        return False

    def validate_file_integrity(self):
        return True

    def main(self, filename, file):

        validate_file = ValidateFile(filename, file)

        ft_check = validate_file.validate_file_type()
        fi_check = validate_file.validate_file_integrity()

        if ft_check and fi_check:
            return True

        return False
