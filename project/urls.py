from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/performances/', include('performance.urls')),  # Συνδέει το urls.py της εφαρμογής performance
    path('api/festivals/', include('festival.urls')),  # Για το app Festival
    path('api/stuff/', include('stuff.urls')),  # Για το app Stuff
]



# Προσθήκη υποστήριξης για τα αρχεία media
if settings.DEBUG:  # Ενεργοποιείται μόνο σε περιβάλλον ανάπτυξης
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
