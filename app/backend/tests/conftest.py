"""Test configuration shared by unit and integration tests.

The environment is set here, before any application module reads its settings,
so that tests never touch the development database.
"""

import os
import tempfile

os.environ["DB_NAME"] = "documind_test"
os.environ["DB_NULL_POOL"] = "true"
# The tests describe the code's defaults, whatever the developer's .env turns on (D87/D88).
os.environ["ANSWER_FACTS"] = "off"
os.environ["SUMMARY_REPAIR"] = "false"
os.environ["ANSWER_TEMPERATURE"] = ""
# Uploaded files written by tests go to a throwaway directory.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="documind-test-data-")

ALLOWED_ORIGIN = "http://127.0.0.1:3000"
