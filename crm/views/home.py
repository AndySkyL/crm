from django.shortcuts import HttpResponse, render, redirect, reverse


def index(request):
    return render(request, 'index.html')
