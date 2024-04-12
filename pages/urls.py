# pages/urls.py
from django.urls import path
from .views import homePageView, homePost, results

urlpatterns = [
    path('', homePageView, name='home'),
    path('homePost/', homePost, name='homePost'),
    path(
        'results/<int:uniformity_of_cell_size>/<int:uniformity_of_cell_shape>/<int:bare_nuclei>/<int:bland_chromatin>/'
        '<int:normal_nucleoli>/<int:clump_thickness>/', results, name='results'),
]
