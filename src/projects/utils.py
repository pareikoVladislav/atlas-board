from core.settings import MEDIA_ROOT


class FileUtils:
    def __init__(
            self,
            dir_project_name: str,
            dir_extension_name: str,
            file_name: str,
            file: bytes
    ):
        self.path = MEDIA_ROOT
        self.dir_project_name = dir_project_name
        self.dir_extension_name = dir_extension_name
        self.file_name = file_name
        self.file = file

    def create_file(self):
        project_path = self.path / self.dir_project_name
        project_path.mkdir(exist_ok=True)
        extension_path = project_path / self.dir_extension_name
        extension_path.mkdir(exist_ok=True)
        file_path = extension_path / self.file_name
        file_path.write(self.file)
        return file_path



