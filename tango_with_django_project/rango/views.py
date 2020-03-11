from django.http import HttpResponse
from django.shortcuts import render

def index(request) :
    context_dict = {'boldmessage': "Sachin, Dhoni, Dravid, Kohli"}
    return render(request, 'rango/index.html', context = context_dict)

def about(request) :
    context_dict = {'name' : "Ajal"}
    return render(request, 'rango/about.html', context = context_dict)