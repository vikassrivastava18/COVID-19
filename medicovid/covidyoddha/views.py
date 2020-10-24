from django.shortcuts import render

from django.http import HttpResponse

yoddha = [

    {
        'name': 'Vikas',
        'title': 'Covid Yoddha 1',
        'content': 'Some little help from our side to Medical team',
        'date':'Octobar 23, 2020'
    },
    {
        'name': 'Datta',
        'title': 'Covid Yoddha 2',
        'content': 'My little contribute to Medical team',
        'date':'Octobar 24, 2020'
    }
]

def home(request):
    context = {
        'yoddha' : yoddha
    }
    return render(request, 'covidyoddha/home.html', context)

def about(request):
    return render(request, 'covidyoddha/about.html', { 'title' : 'About'})