from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from performance.models import Performance
from festival.models import Festival
from django.contrib.auth import get_user_model
from datetime import datetime

class PerformanceModelTest(TestCase):
    """
    Κλάση που περιέχει δοκιμές για το μοντέλο Performance.
    """
    
    def setUp(self):
        """
        Δημιουργεί τους χρήστες, τα festivals και τις παραστάσεις πριν από κάθε τεστ.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )
        self.manager = get_user_model().objects.create_user(
            username='manageruser', email='manageruser@example.com', password='password'
        )
        
        # Δημιουργία Festival
        self.festival = Festival.objects.create(
            title="Test Festival",
            description="This is a test festival.",
            place="Test Place",
            festival_dates="2025-06-01 to 2025-06-10",
            created_by=self.user
        )
        
        # Δημιουργία Performance
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

    def test_performance_title_uniqueness(self):
        """
        Ελέγχει ότι δεν μπορεί να δημιουργηθεί παράσταση με τον ίδιο τίτλο στο ίδιο festival.
        """
        duplicate_performance = Performance(
            title="Test Performance",  # Ίδιος τίτλος
            description="Another performance.",
            kind="Dance",
            duration=1.0,
            starting_time="20:00",
            performance_status="created",
            created_by=self.user,
            festival=self.festival
        )
        
        with self.assertRaises(ValidationError):
            duplicate_performance.clean()  # Πρέπει να αποτύχει λόγω επανάληψης τίτλου

    def test_technical_specs_validation(self):
        """
        Ελέγχει τη λειτουργία του ελέγχου τύπου αρχείων στο πεδίο 'technical_specs'.
        Δημιουργούμε μια προσομοίωση αρχείου με μη έγκυρο τύπο και έπειτα με έγκυρο τύπο.
        """
        # Μη έγκυρος τύπος αρχείου
        invalid_file = SimpleUploadedFile(
            "test_file.exe", 
            b"file_content", 
            content_type="application/x-msdownload"  # Μη έγκυρος τύπος αρχείου
        )
        self.performance.technical_specs = invalid_file

        # Ελέγχουμε αν πετάγεται το ValidationError λόγω του λάθους τύπου αρχείου
        with self.assertRaises(ValidationError):
            self.performance.clean()

        # Έγκυρος τύπος αρχείου
        valid_file = SimpleUploadedFile(
            "test_file.pdf", 
            b"file_content", 
            content_type="application/pdf"  # Έγκυρος τύπος αρχείου
        )
        self.performance.technical_specs = valid_file

        # Δεν πρέπει να πεταχτεί ValidationError για έγκυρο αρχείο
        try:
            self.performance.clean()  # Δεν πρέπει να πετάξουμε εξαίρεση
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for a valid file type")

    def test_performance_status_change(self):
        """
        Ελέγχει αν μπορούμε να αλλάξουμε το status της παράστασης και αν η επικύρωση του status λειτουργεί σωστά.
        """
        self.performance.performance_status = 'submitted'
        self.performance.save()
        
        # Ελέγχουμε ότι το status άλλαξε σε 'submitted'
        self.performance.refresh_from_db()
        self.assertEqual(self.performance.performance_status, 'submitted')

    def test_festival_status_restriction(self):
        """
        Ελέγχει ότι δεν μπορούμε να αλλάξουμε το status της παράστασης αν το festival έχει ανακοινωθεί.
        """
        self.festival.festival_status = 'announced'
        self.festival.save()

        self.performance.performance_status = 'submitted'
        
        with self.assertRaises(ValidationError):
            self.performance.clean()  # Πρέπει να αποτύχει λόγω του περιορισμού του festival status

    def test_festival_title_uniqueness(self):
        """
        Ελέγχει ότι δεν μπορεί να δημιουργηθεί festival με τον ίδιο τίτλο.
        """
        duplicate_festival = Festival(
            title="Test Festival",  # Ίδιος τίτλος
            description="Another festival.",
            place="New Place",
            festival_dates="2025-07-01 to 2025-07-10",
            created_by=self.user
        )
        
        with self.assertRaises(ValidationError):
            duplicate_festival.clean()  # Πρέπει να αποτύχει λόγω επανάληψης τίτλου

    def test_performance_id_auto_increment(self):
        """
        Ελέγχει ότι το πεδίο 'performance_id' αυξάνεται αυτόματα με κάθε νέα παράσταση.
        """
        new_performance = Performance.objects.create(
            title="New Test Performance",
            description="New performance description.",
            kind="Music",
            duration=2.0,
            starting_time="18:00",
            performance_status="created",
            created_by=self.user,
            festival=self.festival
        )
        
        # Ελέγχουμε ότι το performance_id είναι μεγαλύτερο από το προηγούμενο
        self.assertGreater(new_performance.performance_id, self.performance.performance_id)

    def test_performance_manager_field(self):
        """
        Ελέγχει ότι το πεδίο manager στο Performance μπορεί να αποδεχτεί χρήστη.
        """
        self.performance.manager = self.manager
        self.performance.save()

        # Ελέγχουμε ότι το manager είναι σωστά συνδεδεμένος
        self.performance.refresh_from_db()
        self.assertEqual(self.performance.manager, self.manager)

    def test_performance_comments(self):
        """
        Ελέγχει ότι μπορούμε να προσθέσουμε σχόλια σε μια παράσταση και να τα αποθηκεύσουμε.
        """
        self.performance.comments = "Great performance!"
        self.performance.save()

        # Ελέγχουμε ότι τα σχόλια αποθηκεύονται σωστά
        self.performance.refresh_from_db()
        self.assertEqual(self.performance.comments, "Great performance!")

class FestivalModelTest(TestCase):
    """
    Κλάση που περιέχει δοκιμές για το μοντέλο Festival.
    """
    
    def setUp(self):
        """
        Δημιουργεί χρήστη πριν από κάθε τεστ για να δημιουργήσουμε φεστιβάλ.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser', email='testuser@example.com', password='password'
        )

    def test_festival_status_change(self):
        """
        Ελέγχει ότι το status του festival αλλάζει σωστά.
        """
        festival = Festival.objects.create(
            title="Festival Test",
            description="Test festival.",
            place="Test Place",
            festival_dates="2025-06-01 to 2025-06-10",
            created_by=self.user
        )
        
        festival.festival_status = 'submission'
        festival.save()
        
        # Ελέγχουμε ότι το status άλλαξε σωστά
        festival.refresh_from_db()
        self.assertEqual(festival.festival_status, 'submission')

    def test_festival_status_on_decision(self):
        """
        Ελέγχει ότι όταν το status του festival αλλάζει σε 'decision', 
        οι παραστάσεις με status 'approved' πρέπει να ενημερώνονται σε 'rejected'.
        """
        festival = Festival.objects.create(
            title="Festival Status Test",
            description="Test festival status change.",
            place="Test Place",
            festival_dates="2025-07-01 to 2025-07-10",
            created_by=self.user
        )

        # Δημιουργούμε δύο παραστάσεις
        performance1 = Performance.objects.create(
            title="Performance 1",
            description="Performance 1 description.",
            kind="Music",
            duration=2.0,
            starting_time="18:00",
            performance_status="approved",  # Η πρώτη παράσταση έχει status approved
            created_by=self.user,
            festival=festival
        )

        performance2 = Performance.objects.create(
            title="Performance 2",
            description="Performance 2 description.",
            kind="Theater",
            duration=1.5,
            starting_time="20:00",
            performance_status="created",  # Η δεύτερη παράσταση έχει status created
            created_by=self.user,
            festival=festival
        )

        # Αλλάζουμε το status του festival σε 'decision'
        festival.festival_status = 'decision'
        festival.save()

        # Ελέγχουμε ότι η παράσταση με status 'approved' άλλαξε σε 'rejected'
        performance1.refresh_from_db()
        self.assertEqual(performance1.performance_status, 'rejected')

        # Η δεύτερη παράσταση δεν πρέπει να επηρεαστεί
        performance2.refresh_from_db()
        self.assertEqual(performance2.performance_status, 'created')
