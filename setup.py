from setuptools import setup


setup(
    name='surveyor',
    version='0.0.1',
    entry_points={
        'console_scripts': ['test-finder=run_tests:main']
    }
)
