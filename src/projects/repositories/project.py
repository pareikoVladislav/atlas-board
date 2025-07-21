from django.db.models import Q, Count

from src.projects.models.project import Project
from src.projects.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def get_filtered_projects(self, filters: dict = None, ordering: str = None):
        queryset = self.model.objects.all().annotate(members_count=Count('members'))

        filter_kwargs = {}

        if filters:
            if 'owner_username' in filters:
                filter_kwargs['owner__username__icontains'] = filters['owner_username']
            if 'status' in filters:
                filter_kwargs['status'] = filters['status']
            if 'priority' in filters:
                filter_kwargs['priority'] = filters['priority']
            if 'start_date_from' in filters:
                filter_kwargs['start_date__gte'] = filters['start_date_from']
            if 'start_date_to' in filters:
                filter_kwargs['start_date__lte'] = filters['start_date_to']
            if 'members_count_from' in filters:
                filter_kwargs['members_count__gte'] = filters['members_count_from']
            if 'members_count_to' in filters:
                filter_kwargs['members_count__lte'] = filters['members_count_to']

        queryset = queryset.filter(**filter_kwargs)

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
