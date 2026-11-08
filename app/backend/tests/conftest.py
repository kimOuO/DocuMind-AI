"""Test configuration shared by unit and integration tests.

The environment is set here, before any application module reads its settings,
so that tests never touch the development database.
"""

import os
import tempfile

os.environ["DB_NAME"] = "documind_test"
os.environ["DB_NULL_POOL"] = "true"
# The tests run with the answering improvements off and no fixed temperature, whatever the
# developer's .env or the code defaults (D89: inject/true/0.5) say: they describe the
# mechanisms one at a time, turning each on where it is the subject.
# setdefault: the real-model experiment harness (test_navigator_abc_real.py) sets these on
# purpose; it must not be overridden (D93: four batches ran with facts off, repair off and
# the model's default temperature because this used to assign unconditionally).
os.environ.setdefault("ANSWER_FACTS", "off")
os.environ.setdefault("SUMMARY_REPAIR", "false")
os.environ.setdefault("CHECK_NOTES", "true")  # the note tests describe debug mode (D98)
os.environ.setdefault("ANSWER_TEMPERATURE", "")
# Uploaded files written by tests go to a throwaway directory.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="documind-test-data-")

ALLOWED_ORIGIN = "http://127.0.0.1:3000"
