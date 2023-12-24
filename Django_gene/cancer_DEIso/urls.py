from django.urls import path
from . import views

urlpatterns = [
    path('survival_analyis/', views.survival_analyis),
    path('ajax_survival_analyis/', views.ajax_survival_analyis),
    path('survival_screener/', views.survival_screener),
    path('ajax_survival_screener/', views.ajax_survival_screener),
    path('DE_gene_screener/', views.DE_gene_screener_web),
    path('ajax_DE_gene_screener/', views.DE_gene_screener_main),
]