import re
from django.core.files.uploadedfile import UploadedFile

from core.settings import MEDIA_ROOT


class FileUtils:
    def __init__(
            self,
            dir_project_name: str,
            dir_extension_name: str,
            file_name: str,
            file: UploadedFile,
    ):
        self.path = MEDIA_ROOT
        self.dir_project_name = dir_project_name
        self.dir_extension_name = dir_extension_name
        self.file_name = self.normalize_file_name(file_name)
        self.file = file

    def create_file(self):
        project_path = self.path / self.dir_project_name / self.dir_extension_name
        project_path.mkdir(parents=True, exist_ok=True)
        file_path = project_path / self.file_name
        with open(file_path, 'wb') as new_file:
            for chunk in self.file.chunks():
                new_file.write(chunk)
        return str(file_path)

    @staticmethod
    def normalize_file_name(file_name: str) -> str:
        # if not re.match('^[\wА-Яа-я-\s ]+$', str(file_name)):
        if not re.match(r'^[\wА-Яа-яёЁ\s\-.]+$', str(file_name)):
            raise ValueError(f'{file_name} is not a valid file name.')
        new_file_name = file_name.replace(' ', '_')
        return new_file_name







