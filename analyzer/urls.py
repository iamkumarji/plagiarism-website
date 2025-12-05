from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze_text, name='analyze'),
    path('result/<int:document_id>/', views.analysis_result, name='analysis_result'),
    path('history/', views.document_history, name='history'),
    path('api/quick-analyze/', views.quick_analyze, name='quick_analyze'),
    path('learning/', views.learning_center, name='learning'),
]
