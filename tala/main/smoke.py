from smoketest import SmokeTest
from models import Room


class DBConnectivity(SmokeTest):
    def test_retrieve(self):
        cnt = Room.objects.all().count()
        self.assertTrue(cnt > 0)
