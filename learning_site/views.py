from django.shortcuts import render, render_to_response
from django.template import RequestContext

def hello_world(request):
    return render(request, 'home.html')


# HTTP Error 404 Castomizing
def my_404_view(request):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request))
    response.status_code = 404
    return response
