from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("stuff/", include("stuff.urls")),
    path("admin/", admin.site.urls),
    path('api/', include('stuff.urls')),  # Αντικατέστησε το 'myapp' με το όνομα της εφαρμογής σου
]