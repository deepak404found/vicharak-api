from django.contrib import admin
from .models import Vichar, Role, User, Collaborator

# Register your models here.
admin.site.register(Vichar)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Collaborator)
