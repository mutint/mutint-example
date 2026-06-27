from django.shortcuts import render


def index(request):
    return render(request, 'mutint_app/index.html', {})
