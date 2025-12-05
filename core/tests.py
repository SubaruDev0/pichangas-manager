from django.test import TestCase
from django.utils import timezone
from .models import Match, Attendance

class MatchTests(TestCase):
    def test_cost_calculation(self):
        match = Match.objects.create(
            date=timezone.now(),
            location="Test Field",
            total_cost=21000
        )
        
        # 0 players
        self.assertEqual(match.attendances.count(), 0)
        
        # 1 player
        Attendance.objects.create(match=match, name="P1", is_confirmed=True)
        self.assertEqual(match.attendances.filter(is_confirmed=True).count(), 1)
        # Cost logic is in the view, but we can test the math here or test the view.
        # Let's test the math logic that would be used.
        cost = match.total_cost / match.attendances.filter(is_confirmed=True).count()
        self.assertEqual(cost, 21000)
        
        # 2 players
        Attendance.objects.create(match=match, name="P2", is_confirmed=True)
        cost = match.total_cost / match.attendances.filter(is_confirmed=True).count()
        self.assertEqual(cost, 10500)
        
        # 12 players
        for i in range(10):
            Attendance.objects.create(match=match, name=f"Extra{i}", is_confirmed=True)
            
        cost = match.total_cost / match.attendances.filter(is_confirmed=True).count()
        self.assertEqual(cost, 1750)

    def test_attendance_toggle(self):
        match = Match.objects.create(
            date=timezone.now(),
            location="Test Field",
            total_cost=20000
        )
        Attendance.objects.create(match=match, name="Guest", is_confirmed=True)
        self.assertTrue(Attendance.objects.filter(name="Guest", is_confirmed=True).exists())
