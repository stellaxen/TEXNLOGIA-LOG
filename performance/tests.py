from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from performance.models import Performance
from festival.models import Festival
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from unittest.mock import MagicMock

"""
Παρακάτω είναι τα test της εφαρμογής ΧΩΡΙΣ κλήσεις μέσω Rest Api
"""

class PerformanceModelTest(APITestCase):
    """
    Κλάση δοκιμών για το μοντέλο Performance.
    """

    def setUp(self):
        """
        Δημιουργούμε χρήστες, φεστιβάλ και παραστάσεις πριν από κάθε τεστ.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )
        self.manager = get_user_model().objects.create_user(
            username='manageruser', email='manageruser@example.com', password='password'
        )
        
        # Δημιουργία ενός φεστιβάλ
        self.festival = Festival.objects.create(
            title="Test Festival",
            description="This is a test festival.",
            place="Test Place",
            festival_dates="2025-06-01 to 2025-06-10",
            created_by=self.user
        )

        # Δημιουργία παραστάσεων για το API
        self.performance = Performance.objects.create(
            title="Test Performance",
            description="This is a test performance.",
            kind="Theater",
            duration=1.5,
            starting_time="19:00",
            performance_status="created",
            created_by=self.user,
            festival=self.festival
        )

    def test_technical_specs_validation(self):
        """
        Ελέγχει αν η επικύρωση του αρχείου στο πεδίο 'technical_specs' δουλεύει σωστά.
        Ειδικά αν απορρίπτεται αρχείο που δεν είναι PDF ή TXT.
        """
        # Δημιουργία και χρήση mock αρχείου, που είναι ' ψεύτικο ' για αποφυγή πρόσβασης στο σύστημα αρχείων               
        mock_file = MagicMock()
        mock_file.content_type = 'application/pdf'

        # Αντικατάσταση του technical_specs με το mock
        self.performance.technical_specs = mock_file

        # Έλεγχος επικύρωσης
        with self.assertRaises(DjangoValidationError):
            self.performance.clean() # Η μέθοδος clean έχει περιγραφεί στο models.py του performance

    def test_performance_creation(self):
        """
        Δημιουργία νέας παράστασης
        """
        performance = Performance.objects.create(
            title="New Performance",
            description="New performance description.",
            kind="Music",
            duration=2.0,
            starting_time="18:00",
            performance_status="created",
            created_by=self.user,
            festival=self.festival
        )
        # Έλεγχος αν υπάρχει παράσταση με τίτλο New Performance 
        self.assertEqual(performance.title, "New Performance")
        # Έλεγχος αν υπάρχει παράσταση με διάρκεια 2
        self.assertEqual(performance.duration, 2.0)

    def test_performance_update(self):
        """
        Ελέγχει την ενημέρωση παραστάσεων.
        """
        self.performance.title = "Updated Performance"
        self.performance.save()

        updated_performance = Performance.objects.get(id=self.performance.id)
        self.assertEqual(updated_performance.title, "Updated Performance")

    def test_performance_delete(self):
        """
        Ελέγχει τη διαγραφή μίας παράστασης.
        """
        self.performance.delete()
        with self.assertRaises(Performance.DoesNotExist):
            Performance.objects.get(id=self.performance.id)

"""
Παρακάτω είναι τα test της εφαρμογής για κλήσεις μέσω Rest Api
"""

class PerformanceAPITestCase(APITestCase):
    """
    Κλάση δοκιμών για το Performance API.
    """

    def setUp(self):
        """
        Δημιουργούμε ΕΙΚΟΝΙΚΟΥΣ χρήστες, φεστιβάλ και παραστάσεις πριν από κάθε test, τα οποία στο τέλος διαγράφονται
        """
        # Δημιουργία χρηστών
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )
        self.manager = get_user_model().objects.create_user(
            username='manageruser', email='manageruser@example.com', password='password'
        )
        self.admin1 = get_user_model().objects.create_user(
            username='admin1', email='admin1@example.com', password='password'
        )
        self.admin2 = get_user_model().objects.create_user(
            username='admin2', email='admin2@example.com', password='password'
        )

        # Δημιουργία ενός φεστιβάλ
        self.festival = Festival.objects.create(
            title="Test Festival",
            description="This is a test festival.",
            place="Test Place",
            festival_dates="2025-06-01 to 2025-06-10",
            created_by=self.user
        )

        # Δημιουργία παραστάσεων για το API
        self.performance = Performance.objects.create(
            title="Test Performance",
            description="This is a test performance.",
            kind="Theater",
            duration=1.5,
            starting_time="19:00:00",
            performance_status="created",
            created_by=self.user,
            festival=self.festival,
            manager=self.manager,
            rating=4
        )

        self.client.login(username='testuser', password='password')

    def test_get_performances(self):
        """
        Ελέγχει αν η μέθοδος GET επιστρέφει σωστά δεδομένα για τις παραστάσεις.
        """
        url = '/api/performances/'  # Η διεύθυνση URL για το API
        response = self.client.get(url)

        # Ελέγχει ότι η απάντηση είναι 200 OK και επιστρέφει τις παραστάσεις
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Πρέπει να επιστρέψει μία παράσταση, αυτή που ψάξαμε η οποία είναι μοναδική
        self.assertEqual(response.data[0]['title'], 'Test Performance') #Ελέγχει αν ο τίτλος της παράστασης που βρέθηκε είναι Test Performance

    def test_create_performance(self):
        """
        Ελέγχει αν μπορεί να δημιουργηθεί μία νέα παράσταση μέσω της μεθόδου POST.
        """
        url = '/api/performances/'  # Η διεύθυνση URL για το API
        data = {
            'title': 'New Performance',
            'description': 'New performance description.',
            'kind': 'Music',
            'duration': 2.0,
            'starting_time': '18:00:00',  # Ώρα σε πλήρες format
            'performance_status': 'created',
            'festival': self.festival.id,
            'created_by': self.user.id,  # Το ID του χρήστη δημιουργού
            'manager': self.manager.id,  # Το ID του manager
            'rating': 5,  # Παράδειγμα βαθμολογίας
            'administrators': [self.admin1.id, self.admin2.id]  # Βάζει 2 IDs για να έχει 2 administrators το performance
        }

        response = self.client.post(url, data, format='json')

        # Ελέγχει ότι η απάντηση είναι 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Ελέγχει αν ο τίτλος της παράστασης που βρέθηκε είναι New Performance
        self.assertEqual(response.data['title'], 'New Performance')

    def test_create_performance_invalid(self):
        """
        Ελέγχει ότι όταν τα δεδομένα είναι λανθασμένα, επιστρέφεται ένα σφάλμα 400 Bad Request.
        """
        url = '/api/performances/'
        data = {
            'title': '',  # Λάθος δεδομένα (κενός τίτλος)
            'description': 'New performance description.',
            'kind': 'Music',
            'duration': 2.0,
            'starting_time': '18:00',
            'performance_status': 'created',
            'festival': self.festival.id
        }
        
        response = self.client.post(url, data, format='json')

        # Ελέγχει ότι επιστρέφεται σφάλμα 400
        # Γίνεται προσπάθεια δημιουργίας performance χωρίς τίτλο, που είναι υποχρεωτικό πεδίο
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_performance(self):
        """
        Ελέγχει αν μπορεί να ενημερωθεί μία παράσταση μέσω της μεθόδου PATCH.
        """
        url = f'/api/performances/{self.performance.performance_id}/'
        data = {'title': 'Updated Performance'}

        response = self.client.patch(url, data, format='json')

        # Ελέγχει ότι η παράσταση ενημερώθηκε
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ελέγχει αν ο τίτλος της παράστασης που βρέθηκε είναι Updated Performance
        self.assertEqual(response.data['title'], 'Updated Performance')

    def test_update_performance_not_found(self):
        """
        Ελέγχει αν επιστρέφεται σφάλμα 404 όταν η παράσταση δεν βρέθηκε για ενημέρωση.
        """
        url = '/api/performances/999/'  # Μη υπαρκτό ID
        data = {'title': 'Updated Performance'}

        response = self.client.patch(url, data, format='json')

        # Ελέγχει ότι επιστρέφεται σφάλμα 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_performance_permission_denied(self):
        """
        Ελέγχει αν επιστρέφεται σφάλμα 403 όταν ο χρήστης δεν έχει δικαίωμα ενημέρωσης.
        """
        url = f'/api/performances/{self.performance.performance_id}/'
        data = {'title': 'Updated by Another User'}

        # Δημιουργούμε έναν άλλο χρήστη που δεν είναι δημιουργός της παράστασης
        self.client.logout()
        self.client.login(username='manageruser', password='password')

        response = self.client.patch(url, data, format='json')

        # Ελέγχει ότι επιστρέφεται σφάλμα 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_performance(self):
        """
        Ελέγχει αν μπορεί να διαγραφεί μία παράσταση μέσω της μεθόδου DELETE.
        """
        url = f'/api/performances/{self.performance.performance_id}/'

        response = self.client.delete(url)

        # Ελέγχει ότι η παράσταση διαγράφηκε
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Performance deleted successfully.')

    def test_delete_performance_not_found(self):
        """
        Ελέγχει αν επιστρέφεται σφάλμα 404 όταν η παράσταση δεν βρέθηκε για διαγραφή.
        """
        url = '/api/performances/999/'  # Μη υπαρκτό ID

        response = self.client.delete(url)

        # Ελέγχει ότι επιστρέφεται σφάλμα 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_performance_permission_denied(self):
        """
        Ελέγχει αν επιστρέφεται σφάλμα 403 όταν ο χρήστης δεν έχει δικαίωμα διαγραφής.
        """
        url = f'/api/performances/{self.performance.performance_id}/'

        # Δημιουργούμε έναν άλλο χρήστη που δεν είναι δημιουργός της παράστασης
        self.client.logout()
        self.client.login(username='manageruser', password='password')

        response = self.client.delete(url)

        # Ελέγχει ότι επιστρέφεται σφάλμα 403
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_performance_forbidden_due_to_festival_status(self):
        """
        Ελέγχει αν επιστρέφεται σφάλμα 403 όταν το festival έχει status 'announced'.
        """
        # Αλλάζουμε το status του festival σε 'announced'
        self.festival.festival_status = 'announced'
        self.festival.save()

        url = f'/api/performances/{self.performance.performance_id}/'

        response = self.client.delete(url)

        # Ελέγχει ότι επιστρέφεται σφάλμα 403 λόγω status
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
