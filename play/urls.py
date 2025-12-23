from django.urls import path
from .views import barca_vs_real

urlpatterns = [
    path('barca_vs_real', barca_vs_real ,name='barca_vs_real' ),
]