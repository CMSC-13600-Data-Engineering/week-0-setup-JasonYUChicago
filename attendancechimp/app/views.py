from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    return render(request, 'app/index.html', {"test":"SUCCESS!",
                                              "title":"Jason and Victoria's app"})
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
def results(request, question_id):
    response = "You're looking at the results of questoin %s."
    return HttpResponse(response % question_id)
def vote(request, question_id):
    return HttpResponse("You're voting on question %s" % question_id)