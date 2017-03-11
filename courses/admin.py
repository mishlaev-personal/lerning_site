from django.contrib import admin
from datetime import date

# Register your models here.
from . import models


class TextInline(admin.StackedInline):
    model = models.Text


class QuizInline(admin.StackedInline):
    model = models.Quiz


class YearListFilter(admin.SimpleListFilter):
    title = 'year created'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        return (
            ('2016', '2016'),
            ('2017', '2017')
        )

    def queryset(self, request, queryset):
        if self.value() == '2016':
            return queryset.filter(created_at__gte=date(2016, 1, 1),
                                   created_at__lte=date(2016, 12, 31))
        if self.value() == '2017':
            return queryset.filter(created_at__gte=date(2017, 1, 1),
                                   created_at__lte=date(2017, 12, 31))


class CourseAdmin(admin.ModelAdmin):
    inlines = [TextInline, QuizInline]
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'published', YearListFilter, 'teacher', 'subject']
    list_display = [
        'title',
        'published',
        'teacher',
        'subject',
        'time_to_complete',
        'total_steps',
        'created_at'
        ]
    list_editable = ['published', 'teacher', 'subject']


class TextAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'published', 'order', 'description', 'content']
    search_fields = ['title', 'description']
    list_filter = ['course', 'published']
    list_display = ['title', 'course', 'published']
    list_display_links = ['course']


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'published', 'order', 'description', 'total_questions']
    search_fields = ['title', 'description']
    list_filter = ['course', 'published']
    list_display = ['title', 'course', 'published']
    list_display_links = ['course']


class AnswerAdmin(admin.ModelAdmin):
    list_filter = ['question', 'published']
    list_display = ['text', 'correct', 'short_question', 'published']
    list_display_links = ['short_question']
    list_editable = ['text', 'correct']

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion)
admin.site.register(models.TrueFalseQuestion)
admin.site.register(models.Answer, AnswerAdmin)


admin.site.site_header = "Learning Site administration"
