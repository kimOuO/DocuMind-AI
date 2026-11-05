"""Test configuration shared by unit and integration tests.

The environment is set here, before any application module reads its settings,
so that tests never touch the development database.
"""

import os

os.environ["DB_NAME"] = "documind_test"
os.environ["DB_NULL_POOL"] = "true"

ALLOWED_ORIGIN = "http://127.0.0.1:3000"
