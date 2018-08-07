from django.contrib import admin
from task import models
from task import forms


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    form = forms.GroupForm
    exclude = ('parent_check', 'slug')


@admin.register(models.Element)
class ElementAdmin(admin.ModelAdmin):
    form = forms.ElementForm
    exclude = ('group_check', 'slug')
