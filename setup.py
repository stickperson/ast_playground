from setuptools import setup


setup(
    name='ast-playground',
    version='1',
    entry_points={
        'console_scripts': ['ast-playground=run_tests:main']
    }
)
