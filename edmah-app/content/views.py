from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Category, Formation
from events.models import Event

from .models import FAQ, Article, ArticleCategory, GalleryItem


def index_view(request):
    context = {
        'featured_formations': Formation.objects.filter(is_published=True, is_featured=True)[:3],
        'next_event': Event.objects.filter(is_published=True, start_datetime__gte=timezone.now()).order_by('start_datetime').first(),
        'latest_articles': Article.objects.filter(is_published=True)[:3],
    }
    return render(request, 'index.html', context)


def about_view(request):
    return render(request, 'about.html')


def formations_view(request):
    context = {
        'formations': Formation.objects.filter(is_published=True).select_related('category').prefetch_related('highlights'),
        'categories': Category.objects.all(),
    }
    return render(request, 'formations.html', context)


def cours_view(request):
    if request.user.is_authenticated:
        return redirect('apprenant_dashboard')
    return redirect('login')


def evenements_view(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(is_published=True, start_datetime__gte=now)
    context = {
        'upcoming_events': upcoming_events,
        'past_events': Event.objects.filter(is_published=True, start_datetime__lt=now),
        'featured_event': upcoming_events.first(),
    }
    return render(request, 'evenements.html', context)


def gallerie_view(request):
    items = GalleryItem.objects.filter(is_published=True)
    categories = sorted({item.category for item in items if item.category})
    context = {'gallery_items': items, 'categories': categories}
    return render(request, 'gallerie.html', context)


def blog_view(request):
    articles = Article.objects.filter(is_published=True).select_related('category')

    query = request.GET.get('q', '').strip()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(body__icontains=query))

    category_slug = request.GET.get('category', '').strip()
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    paginator = Paginator(articles, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'articles': page_obj.object_list,
        'categories': ArticleCategory.objects.all(),
        'popular_articles': Article.objects.filter(is_published=True)[:3],
        'query': query,
        'active_category': category_slug,
    }
    return render(request, 'blog.html', context)


def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'article_detail.html', {'article': article})


def contact_view(request):
    context = {'faqs': FAQ.objects.filter(is_published=True)}
    return render(request, 'contact.html', context)


def inscriptions_view(request):
    context = {'formations': Formation.objects.filter(is_published=True)}
    return render(request, 'inscriptions.html', context)


def certifications_view(request):
    return render(request, 'certifications.html')
