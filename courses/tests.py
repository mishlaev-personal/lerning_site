from django.test import TestCase, Client
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Course, Text, Quiz


class CourseModelTests(TestCase):
    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write RegEx in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)


class StepModelTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write RegEx in Python"
        )

    def test_text_creation(self):
        step = Text.objects.create(
            title="Step test",
            description="Step Step Desc",
            content="jkwrj r eljkn reljn er  erjklnerw lkjn  wegrljknrgw ljknrq glnjr egl jngrwe l nj wegrlnj",
            course=self.course
        )
        self.assertIn(step, self.course.text_set.all())

    def test_quiz_creation(self):
        quiz = Quiz.objects.create(
            title="Quiz test",
            description="Quiz Quiz Desc",
            total_questions=10,
            course=self.course
        )
        self.assertIn(quiz, self.course.quiz_set.all())


class CourseViewTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write RegEx in Python"
        )
        self.course2 = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write RegEx in Python"
        )
        self.text = Text.objects.create(
            title="Text Title",
            description="Text Text",
            content="Text Text njkfvkljfvm;kfvk kmk egkl egwr",
            course=self.course
        )
        self.quiz = Quiz.objects.create(
            title="Quiz Step Title",
            description="Quiz Text",
            total_questions=10,
            course=self.course
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail', kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/course_detail.html')
        self.assertContains(resp, self.course.title)

    def test_text_detail_view(self):
        resp = self.client.get(reverse('courses:text',
                                       kwargs=
                                       {'course_pk': self.course.pk,
                                       'step_pk': self.text.pk}
                                       ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.text, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/text_detail.html')
        self.assertContains(resp, self.text.title)

    def test_quiz_detail_view(self):
        resp = self.client.get(reverse('courses:quiz',
                                       kwargs=
                                       {'course_pk': self.course.pk,
                                       'step_pk': self.quiz.pk}
                                       ))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.quiz, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/quiz_detail.html')
        self.assertContains(resp, self.quiz.title)
