import sys

if len(sys.argv) > 1 and sys.argv[1] == "test":
    from .unit_tests import run_tests
    run_tests()