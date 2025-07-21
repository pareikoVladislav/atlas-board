from django.db.models import Q, Count

from src.projects.models.project import Project
from src.projects.repositories.base import BaseRepository


class ProjectRepository(BaseRepository):
    def __init__(self):
        super().__init__(Project)

    def get_filtered_projects(self, filters: dict = None, ordering: str = None):
        queryset = self.model.objects.all().annotate(members_count=Count('members'))

        q = Q()
        if filters:
            if 'owner_username' in filters:
                q &= Q(owner__username__icontains=filters['owner_username'])

            if 'status' in filters:
                q &= Q(status=filters['status'])

            if 'priority' in filters:
                q &= Q(priority=filters['priority'])

            if 'start_date_from' in filters:
                q &= Q(start_date__gte=filters['start_date_from'])

            if 'start_date_to' in filters:
                q &= Q(start_date__lte=filters['start_date_to'])

            if 'members_count_from' in filters:
                q &= Q(members_count__gte=filters['members_count_from'])

            if 'members_count_to' in filters:
                q &= Q(members_count__lte=filters['members_count_to'])

        queryset = queryset.filter(q)

        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset
