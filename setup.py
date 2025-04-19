from setuptools import setup

APP = ['ShooterGame.py']  # Change this to your script name
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)