from django.shortcuts import render

def home(request):
    template_name = 'home.html'
    context = {
        'title': 'home',
    }
    return render(request, template_name, context)
