from django import template
from courses.models import Course


register = template.Library()

@register.simple_tag
def newest_course():
    ''' Gets the most recent course that was added to the library. '''
    return Course.objects.latest('created_at')


@register.inclusion_tag('courses/course_nav.html')
def nav_courses_list():
    '''Returns dictionary of course to display as nav panel'''
    courses = Course.objects.all()
    return {'courses': courses}

@register.filter('time_estimate')
def time_estimate(word_count):
    '''Estimates the number of minutes to compleate a step based on the passed-in wordcount'''
    minutes = round(word_count/20)
    return minutes