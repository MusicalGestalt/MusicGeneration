import platform
import sys

if len(sys.argv) < 2:
    from .unit_tests import *
    main()
else:
    if "Darwin" in platform.platform():
        from .osx import main
        main()