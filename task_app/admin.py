from django.contrib import admin
from .models import Task, TaskComment
from django import forms
from django.utils.html import format_html
# class TaskAdminForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'status']

class TaskCommentInline(admin.TabularInline):
    model = TaskComment
    extra = 1  # Number of extra blank forms to display
    fields = ['creator','comment', 'created_at']
    readonly_fields = ['created_at' ,'creator']
    
    def has_change_permission(self, request, obj=None):
        return False  # To prevent editing existing comments if needed
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

     

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'due_date', 'assigned_to_list')
    inlines = [TaskCommentInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(assigned_to=request.user)

    def assigned_to_list(self, obj):
        return ", ".join([user.username for user in obj.assigned_to.all()])
    assigned_to_list.short_description = 'Assigned to'

    def get_form(self, request, obj=None, **kwargs):
        form = super(TaskAdmin, self).get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            # Disable all fields except 'status' for non-superusers
            disabled_fields = {field_name: form.base_fields[field_name].disabled for field_name in form.base_fields if field_name != 'status'}
            for field_name in disabled_fields:
                form.base_fields[field_name].disabled = True
        return form
    
    def get_fields(self, request, obj=None):
        fields = super(TaskAdmin, self).get_fields(request, obj)
        if not request.user.is_superuser:
            # Exclude some fields if the user is not a superuser
            fields = [field for field in fields if field not in ['created_at', 'assigned_to']]
        return fields
    
    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.assigned_to.filter(id=request.user.id).exists()
        return super().has_change_permission(request, obj)
        

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, TaskComment) and not instance.pk:
                instance.creator = request.user  # Set the creator to the current user
            instance.save()
        formset.save_m2m()
    
        



class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('comment_short', 'task', 'created_at')

    def has_module_permission(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(task__assigned_to=request.user)

    def comment_short(self, obj):
        return format_html("<span>{}</span>", obj.comment[:50])
    comment_short.short_description = 'Comment'

    def has_change_permission(self, request, obj=None):
        return True  # To prevent editing comments

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    


admin.site.register(TaskComment, TaskCommentAdmin)

admin.site.register(Task, TaskAdmin)