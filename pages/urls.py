# pages/urls.py
from django.urls import path
from .views import homePageView, homePost, results

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path(
        'results/<int:clump_thickness>/<int:bland_chromatin>/<int:marginal_adhesion>/<int:bare_nuclei>/<int:single_epithelial_cell_size>/',
        results, name='results'),
]
