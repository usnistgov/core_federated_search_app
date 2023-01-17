import json
from unittest.mock import Mock


class MockResponse(Mock):
    data: str = None

    def json(self):
        return json.loads(self.data)
