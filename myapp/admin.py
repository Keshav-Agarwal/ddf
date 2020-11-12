from django.contrib import admin
from. models import CompletedTasks, Tasks
from django.contrib.auth.models import Permission


# Register your models here.
admin.site.register(Tasks)
admin.site.register(CompletedTasks)
admin.site.register(Permission)