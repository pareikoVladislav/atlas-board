
class BaseRepository:
    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        ...

    def get_all(self):
        ...

    def get_by_id(self, project_id):
        ...

    def update_by_id(self, project_id, **kwargs):
        ...