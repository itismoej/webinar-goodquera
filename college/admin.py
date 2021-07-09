from django.contrib import admin

from .models import College, Lesson


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
