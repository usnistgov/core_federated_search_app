""" Fixtures files for Instance
"""
from core_federated_search_app.components.instance.models import Instance
from core_main_app.utils.datetime import datetime_now
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)


class InstanceFixtures(FixtureInterface):
    """Instance fixtures"""

    data_1 = None
    data_collection = None

    def insert_data(self):
        """Insert a set of Data.

        Returns:

        """
        # Make a connexion with a mock database
        self.generate_data_collection()

    def generate_data_collection(self):
        """Generate a Data collection.

        Returns:

        """
        self.data_1 = Instance(
            name="name_1",
            endpoint="http://127.0.0.1:8000/",
            access_token="token",
            refresh_token="refresh",
            expires=datetime_now(),
        )
        self.data_1.save()
        self.data_collection = [self.data_1]
