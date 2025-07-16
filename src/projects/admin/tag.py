from django.contrib import admin

from src.projects.models.tag import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20
    fields = ('name',)
