# bank_app/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('ai-suggestion/', views.ai_suggestion_api, name='ai_suggestion_api'),
    path('download-pdf/<int:app_id>/', views.download_pdf, name='download_pdf'),
    path('success/', views.success_page, name='success'),
]

# Media files serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)