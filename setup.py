from setuptools import setup, find_packages

setup(
    name="ProjectName",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Hier können zusätzliche Abhängigkeiten eingetragen werden
    ],
    entry_points={
        'console_scripts': [
            # Optional: Falls eine main()-Funktion definiert wird
            # 'projectname=main:main',
        ],
    },
)
