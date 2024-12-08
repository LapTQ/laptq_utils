from setuptools import find_packages, setup


setup(
    name="laptq_pyutils",
    packages=find_packages(
        include=[
            "laptq_pyutils",
        ]
    ),
    version="0.1.0",
    description="Python utilities for common tasks",
    author="Tran Quoc Lap",

    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)
