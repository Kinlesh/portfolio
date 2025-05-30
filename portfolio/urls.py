from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import jobs.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', jobs.views.home, name="home"),
    path("jobs/<int:job_id>", jobs.views.detail, name="detail"),
    path("chatbot/", include("chatbot.urls")),  # chatbot uygulamasını /chatbot/ yoluna ekliyoruz
]

# Statik ve medya dosyaları için ayarlar
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
