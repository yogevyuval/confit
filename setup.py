from setuptools import setup, find_packages

setup(
    name="confit",
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'confit = confit.main:generate_config',
        ]
    }
)
