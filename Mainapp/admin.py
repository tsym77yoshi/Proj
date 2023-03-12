from django.contrib import admin
from .models import *

class AreaAdmin(admin.ModelAdmin):
    list_display=('name','IsAvailable','helptext')

class RoomAdmin(admin.ModelAdmin):
    list_display=('name','IsNeedCheck','IsAvailable','helptext')
    #list_editable=('name','IsNeedCheck','IsAvailable','helptext')

class EventAdmin(admin.ModelAdmin):
    list_display=('date','title')
    #list_editable=('date','title')

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id','date','time','place','organization','StudentNum','teacherSeal','affairsSeal','roomSeal','state','created_datetime','updated_datetime')
    list_display_links = ('date','time','place','organization','StudentNum','teacherSeal','affairsSeal','roomSeal')
    list_per_page=100

admin.site.register(Area,AreaAdmin)
admin.site.register(Room,RoomAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Schedule,ScheduleAdmin)