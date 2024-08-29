
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("",include('api.urls'), name="index"),
    path('api/', include('api.urls'), name="api_endpoints"),
]
