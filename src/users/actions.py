from django.contrib import admin, messages

@admin.action(description="Activate selected users")
def activate_users(self, request, queryset):
    updated = queryset.update(is_active=True, deleted=False, deleted_at=None)
    self.message_user(
        request,
        f"Successfully activated {updated} users",
        messages.SUCCESS
    )


@admin.action(description="Deactivate selected users")
def deactivate_users(self, request, queryset):
    updated = queryset.update(is_active=False)
    self.message_user(
        request,
        f"Successfully deactivated {updated} users",
        messages.SUCCESS
    )
