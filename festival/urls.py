# festival/urls.py

# urlpatterns = [
#     path('', FestivalAPIView.as_view(), name='festival-list-create'),
# ]


from django.urls import path
from .views import FestivalAPIView

urlpatterns = [
    # Διαδρομή για το endpoint που θα εμφανίζει όλα τα φεστιβάλ και για την δημιουργία νέου φεστιβάλ
    path('', FestivalAPIView.as_view(), name='festival-list-create'),

    # Διαδρομή για το endpoint για ένα συγκεκριμένο φεστιβάλ με το id του (π.χ. /api/festivals/1/)
    path('<int:pk>/', FestivalAPIView.as_view(), name='festival-detail'),
]
