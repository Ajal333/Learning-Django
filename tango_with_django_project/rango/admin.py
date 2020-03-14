# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from rango.models import Category, Page


# Register your models here.

class PageAdmin(admin.ModelAdmin) :
    list_display = ('title','category','url','views',) 

class CatAdmin(admin.ModelAdmin) :
    list_display = ('name','views','likes')
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CatAdmin)
admin.site.register(Page,PageAdmin)