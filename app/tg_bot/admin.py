from django.contrib import admin

from .models import *


@admin.register(Particiant)
class AdminParticiant(admin.ModelAdmin):
    list_display = ('name', 'email')


@admin.register(Event)
class AdminSEvent(admin.ModelAdmin):
    list_display = ('date',)


@admin.register(Lecture)
class AdminLecture(admin.ModelAdmin):
    list_display = ('get_time', 'title', 'speaker', 'start', 'event',)
    list_filter = ('event',)
    ordering = ('start',)

    def get_time(self, obj):
        lecture = Lecture.objects.get(pk=obj.pk)
        return f'{lecture.start} - {lecture.end}'
