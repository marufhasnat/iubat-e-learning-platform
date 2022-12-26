from django.contrib import admin
from .models import *


class what_you_learn_TabularLine(admin.TabularInline):
    model = What_you_learn


class Requirements_TabularLine(admin.TabularInline):
    model = Requirements


class Lesson_TabularLine(admin.TabularInline):
    model = Lesson


class Video_TabularLine(admin.TabularInline):
    model = Video


class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TabularLine, Requirements_TabularLine, Lesson_TabularLine, Video_TabularLine)


# Register your models here.
admin.site.register(Categories)
admin.site.register(Instructor)
admin.site.register(Course, course_admin)
admin.site.register(Level)
admin.site.register(What_you_learn)
admin.site.register(Requirements)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Review)
