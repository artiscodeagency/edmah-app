from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

def formations_view(request):
    return render(request, 'formations.html')

def cours_view(request):
    return render(request, 'cours.html')

def evenements_view(request):
    return render(request, 'evenements.html')

def gallerie_view(request):
    return render(request, 'gallerie.html')

def blog_view(request):
    return render(request, 'blog.html')

def contact_view(request):
    return render(request, 'contact.html')

def inscriptions_view(request):
    return render(request, 'inscriptions.html')

def certifications_view(request):
    return render(request, 'certifications.html')
