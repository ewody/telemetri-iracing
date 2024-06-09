from cx_Freeze import setup, Executable

setup(
    name = "iRacing Telemetry",
    version = "0.1",
    description = "Application de télémétrie pour iRacing",
    executables = [Executable("main.py", icon="teleimage.ico")]
)
