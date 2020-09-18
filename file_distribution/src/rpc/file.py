from src.file_service import FileService


def get_file(**kwargs):
    file_path = FileService.get_files(kwargs["type"], kwargs.get("num_files", 1))
    with open(file_path, "rb") as content_file:
        content = content_file.read()
        return content  # .encode()
