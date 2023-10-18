from django.contrib import admin
from .models import *
from django import forms
from guardian.admin import GuardedModelAdmin

admin.site.register(Business)


# class TypeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'business')


# class UniversalEntitiesAdmin(admin.ModelAdmin):
#     list_display = ('xname','xbusiness', 'xtype', )


# admin.site.register(Type, TypeAdmin)
# admin.site.register(UniversalEntities, UniversalEntitiesAdmin)
