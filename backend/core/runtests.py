import os
import sys

# add core to sys path
cwd = os.getcwd()
os.chdir("..")
sys.path.append(os.path.join(os.getcwd()))
sys.path.append(os.path.join(cwd, "apps", "pennies"))
os.chdir(cwd)

import django  # noqa: E402
from django.conf import settings  # noqa: E402
from django.test.utils import get_runner  # noqa: E402

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
