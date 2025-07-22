from pathlib import Path
from rest_framework import serializers

from src.projects.models import ProjectFile
from src.projects.repositories import ProjectFileRepository
from src.users.dto import UserShortDTO
from src.projects.services.service_responce import FileType
from src.projects.utils import FileUtils

def validate_file_extension(file_name: str) -> None:
    extensions = FileType.choices()
    extension = Path(file_name).suffix[1:]
    if not extension in extensions:
        raise serializers.ValidationError(
            f"{extension} must be in {extensions}"
        )

def validate_file_size(file) -> None:
    if file.size / 1024 / 1024 > 2:
        raise serializers.ValidationError(
            "Max file size is greater than 2 MB"
        )


class ProjectFileDTO(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = (
            'id',
            'name',
            'file_path',
            'is_public',
        )


class CreateProjectFileDTO(serializers.ModelSerializer):
    file = serializers.FileField(validators=[
        validate_file_extension,
        validate_file_size,
    ]
    )

    class Meta:
        model = ProjectFile
        fields = (
            'name',
            'file_path',
            'uploaded_by',
            'file'
        )

    def create(self, validated_data):
        repository = ProjectFileRepository()
        project = self.context['project']
        user = self.context['user']
        file = validated_data.pop('file')
        file_manager = FileUtils(
            dir_project_name=project.name,
            dir_extension_name=Path(file.name).suffix[1:],
            file_name=file.name,
            file=file
        )
        file_path = file_manager.create_file()
        validated_data.update(
            {
                "file_path": file_path,
                "uploaded_by": user,
                "name": file.name,
            }
        )
        file = repository.create(**validated_data)
        file.projects.add(project)
        return file






class ProjectFileDetailDTO(serializers.ModelSerializer):
    uploaded_by = UserShortDTO(read_only=True)

    class Meta:
        model = ProjectFile
        fields = (
            'id',
            'name',
            'file_path',
            'is_public',
            'uploaded_by',
            'created_at',
        )

