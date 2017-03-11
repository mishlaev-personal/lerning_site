from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars


# Create your models here.
class Course(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User)
    subject = models.CharField(default='', max_length=100)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def time_to_complite(self):
        from courses.templatetags.course_extras import time_estimate
        return time_estimate(len(self.description.split()))


class Step(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    published = models.BooleanField(default=False)
    # content = models.TextField(blank=True, default='')

    class Meta:
        abstract = True
        ordering = ['order',]

    def __str__(self):
        return self.title


class Text(Step):
    content = models.TextField(blank=True, default='')
    step_type = 'Text'

    def get_absolute_url(self):
        return reverse('courses:text', kwargs={
            'course_pk': self.course_id,
            'step_pk': self.id
        })


class Quiz(Step):
    total_questions = models.IntegerField(default=4)
    step_type = 'Quiz'
    times_taken = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name_plural = "Quizzes"

    def get_absolute_url(self):
        return reverse('courses:quiz', kwargs={
            'course_pk': self.course_id,
            'step_pk': self.id
        })


class Question(models.Model):
    quiz = models.ForeignKey(Quiz)
    order = models.IntegerField(default=0)
    prompt = models.TextField()
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order',]

    def get_absolute_url(self):
            return self.quiz.get_absolute_url()

    def __str__(self):
            return self.prompt


class MultipleChoiceQuestion(Question):
    shuffle_answers = models.BooleanField(default=False)


class TrueFalseQuestion(Question):
    pass


class Answer(models.Model):
    question = models.ForeignKey(Question)
    order = models.IntegerField(default=0)
    text = models.CharField(max_length=255)
    correct = models.BooleanField(default=False)
    published = models.BooleanField(default=False)


    class Meta:
        ordering = ['order',]

    def __str__(self):
        return self.text

    @property
    def short_question(self):
        return truncatechars(self.question, 50)
