from django.contrib import admin
from django.urls import include, path

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/performances/', include('performance.urls')),  # Για το app Performance
#     path('api/festivals/', include('festival.urls')),  # Για το app Festival
#     path('api/stuff/', include('stuff.urls')),  # Για το app Stuff
# ]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('performance.urls')),  # Συνδέει το urls.py της εφαρμογής performance
    path('api/festivals/', include('festival.urls')),  # Για το app Festival
    path('api/stuff/', include('stuff.urls')),  # Για το app Stuff
]
