import json
from unittest.mock import Mock, MagicMock


class MockResponse(Mock):
    data: str = None
    status_code: int = 0
    content = MagicMock()

    def json(self):
        return json.loads(self.data)
