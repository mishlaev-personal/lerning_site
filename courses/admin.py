from django.contrib import admin
from datetime import date

# Register your models here.
from . import models


def make_published(self, request, queryset):
    rows_updated = queryset.update(status='p', published=True)
    rows_updated_message(self, request, rows_updated)


def make_in_review(self, request, queryset):
    rows_updated = queryset.update(status='r', published=False)
    rows_updated_message(self, request, rows_updated)


def make_in_progress(self, request, queryset):
    rows_updated = queryset.update(status='i', published=False)
    rows_updated_message(self, request, rows_updated)


def rows_updated_message(self, request, rows_updated):
    if rows_updated == 1:
        message_bit = "1 story was"
    else:
        message_bit = "%s courses were" % rows_updated
    self.message_user(request, "%s successfully updated." % message_bit)


make_published.short_description = 'Mark selected as Published'


class TextInline(admin.StackedInline):
    model = models.Text


class QuizInline(admin.StackedInline):
    model = models.Quiz


class AnswerTabed(admin.TabularInline):
    model = models.Answer


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
        'status'
        ]
    list_editable = ['teacher', 'subject', 'status']
    actions = [make_published, make_in_progress, make_in_review]


class TextAdmin(admin.ModelAdmin):
    # fields = ['course', 'title', 'published', 'order', 'description', 'content']
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'published', 'order', 'description',)
        }),
        ('Add content', {
            'fields':  ('content',),
            'classes': ('collapse',)
        })
    )
    search_fields = ['title', 'description']
    list_filter = ['course', 'published']
    list_display = ['title', 'course', 'published']
    list_display_links = ['title', 'course']
    radio_fields = {'course': admin.HORIZONTAL}


class QuizAdmin(admin.ModelAdmin):
    fields = ['course', 'title', 'published', 'order', 'description', 'total_questions']
    search_fields = ['title', 'description']
    list_filter = ['course', 'published']
    list_display = ['title', 'course', 'published']
    list_display_links = ['course']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerTabed,]
    list_filter = ['quiz', 'published']
    search_fields = ['prompt']
    list_display = ['prompt', 'quiz', 'order']
    list_editable = ['quiz', 'order']

admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Text, TextAdmin)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.MultipleChoiceQuestion, QuestionAdmin)
admin.site.register(models.TrueFalseQuestion, QuestionAdmin)
admin.site.register(models.Answer)


admin.site.site_header = "Learning Site administration"
