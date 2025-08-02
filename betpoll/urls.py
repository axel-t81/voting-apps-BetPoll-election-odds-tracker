from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('odds/', include('odds.urls')),
    path('', RedirectView.as_view(pattern_name='odds:home'), name='home'),
]