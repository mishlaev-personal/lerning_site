from itertools import chain
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages

from . import forms
from . import models


def course_list(request):
    courses = models.Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_detail(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),
                   key=lambda step: step.order)
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'steps': steps
    })


def text_detail(request, course_pk, step_pk):
    text = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/text_detail.html', {'step': text})


def quiz_detail(request, course_pk, step_pk):
    quiz = get_object_or_404(models.Quiz, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/quiz_detail.html', {'step': quiz})


@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS, "Quiz Added!")
            return HttpResponseRedirect(quiz.get_absolute_url())

        else:
            messages.add_message(request, messages.ERROR, "Form is not valid!")

    return render(request, 'courses/quiz_form.html', {'form': form,
                                                      'course': course
                                                      })


@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk)
    form = forms.QuizForm(instance=quiz)
    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated {}".format(form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form,
                                                      'course': quiz.course})


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':
        form_class = forms.TrueFalseQuestionForms
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Added question')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {'quiz': quiz,
                                                      'form': form})


@login_required
def quiz_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question,
                                 pk=question_pk, quiz_id=quiz_pk)
    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForms
        question = question.truefalsequestion
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion
    form = form_class(instance=question)

    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updates question')
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {'form': form,
                                                          'quiz': question.quiz})


@login_required
def answer_form(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)

    formset = forms.AnswerFormSet(queryset=question.answer_set.all())

    if request.method == "POST":
        formset = forms.AnswerFormSet(request.POST,
                                      queryset=question.answer_set.all())
        if formset.is_valid():
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, "Added answers!")
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, "courses/answer_form.html", {'question': question,
                                                        'formset': formset})
