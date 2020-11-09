from setuptools import setup


setup(
    name='test-finder',
    version='1',
    entry_points={
        'console_scripts': ['test-finder=run_tests:main']
    }
)
