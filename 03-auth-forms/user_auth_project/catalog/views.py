from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Item

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Track recently viewed items in session (list of item pk)
    recent = request.session.get('recent_items', [])
    if pk in recent:
        recent.remove(pk)
    recent.insert(0, pk)
    # Optionally limit to last N items
    recent = recent[:5]
    request.session['recent_items'] = recent

    context = {
        'item': item,
        'recent': [Item.objects.get(pk=i) for i in recent if Item.objects.filter(pk=i).exists()],
    }
    return render(request, 'catalog/item_detail.html', context)

def preferences(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        # store preference in session
        request.session['theme_pref'] = theme
        # optionally set expiry for this session data
        request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
        return redirect('session_summary')

    # GET: show form
    current = request.session.get('theme_pref', 'light')
    return render(request, 'catalog/preferences.html', {'current': current})

def session_summary(request):
    # Read from session
    recent = request.session.get('recent_items', [])
    theme = request.session.get('theme_pref', 'light')
    context = {
        'recent': Item.objects.filter(pk__in=recent),
        'theme': theme,
        'expiry_age': request.session.get_expiry_age(),
    }
    return render(request, 'catalog/session_summary.html', context)
