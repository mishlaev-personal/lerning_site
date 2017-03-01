from django.contrib import admin

# Register your models here.
from .models import Course, Text


class TextInline(admin.StackedInline):
    model = Text


class CourseAdmin(admin.ModelAdmin):
    inlines = [TextInline, ]
    pass


admin.site.register(Course, CourseAdmin)
admin.site.register(Text)
