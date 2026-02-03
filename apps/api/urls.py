from django.urls import path
from .views import CalculationView, IngestionView
from .search_views import SearchView
from .law_views import LawDetailView, LawListView

urlpatterns = [
    path('calculate/', CalculationView.as_view(), name='calculate'),
    path('search/', SearchView.as_view(), name='search'),
    path('ingest/', IngestionView.as_view(), name='ingest'),
    path('laws/', LawListView.as_view(), name='law-list'),
    path('laws/<str:law_id>/', LawDetailView.as_view(), name='law-detail'),
]
