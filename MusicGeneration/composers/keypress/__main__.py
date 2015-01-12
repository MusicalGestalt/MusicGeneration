import platform

if "Darwin" in platform.platform():
    from .osx import main
    main()