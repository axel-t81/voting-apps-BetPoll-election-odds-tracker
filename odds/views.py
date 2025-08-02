from django.views.generic import TemplateView, ListView
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import ElectionOdds, Party, Bookmaker
from django.utils import timezone

class HomeView(TemplateView):
    template_name = "odds/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parties'] = Party.objects.filter(active=True)
        context['bookmakers'] = Bookmaker.objects.filter(active=True)
        return context

class OddsListView(ListView):
    template_name = "odds/odds_list.html"
    context_object_name = 'odds_list'
    
    def get_queryset(self):
        return ElectionOdds.objects.select_related(
            'party', 'bookmaker'
        ).filter(
            party__active=True,
            bookmaker__active=True
        ).order_by('-date', 'party__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_updated'] = timezone.now()
        return context

def chart_data(request):
    """API endpoint for chart data"""
    odds = ElectionOdds.objects.select_related(
        'party', 'bookmaker'
    ).filter(
        party__active=True,
        bookmaker__active=True
    ).order_by('date')

    data = {
        'labels': [],
        'datasets': {}
    }
    
    # Initialize datasets for each party
    for party in Party.objects.filter(active=True):
        data['datasets'][party.name] = {
            'label': party.name,
            'data': [],
            'borderColor': party.color,
            'fill': False
        }
    
    # Group data by date
    for odd in odds:
        date_str = odd.date.strftime('%Y-%m-%d')
        if date_str not in data['labels']:
            data['labels'].append(date_str)
        data['datasets'][odd.party.name]['data'].append(float(odd.probability))
    
    # Convert datasets dict to list for Chart.js
    data['datasets'] = list(data['datasets'].values())
    
    return JsonResponse(data)