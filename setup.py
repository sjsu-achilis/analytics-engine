from setuptools import setup, find_packages

dependencies = [
]

setup(
    name="achlib",
    version="0.1",
    packages=find_packages(),
    install_requires=dependencies,
    package_data={"": ["*.ini"]},
)
