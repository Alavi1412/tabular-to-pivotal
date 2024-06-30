from setuptools import find_packages, setup

setup(
    name="tabular_to_pivotal",
    python_requires=">=3.11",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pydantic==2.7.4"],
    entry_points={
        "console_scripts": [
            "tabular_to_pivotal=tabular_to_pivotal:main",
        ],
    },
)
