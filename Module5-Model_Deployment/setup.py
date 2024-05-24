#!\usr\bin\python
"""Setuptools-based installation."""
import os
from pathlib import Path
from typing import List

from setuptools import find_packages, setup


readme = (Path(__file__).parent / "README.md").read_text()


REQUIREMENTS_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "requirements.txt"
)
with open(REQUIREMENTS_PATH, "r", encoding="utf-8") as requirements_file:
    install_requires = requirements_file.read().splitlines()

setup(
    name="icmd_project",
    version="0.0.1",
    author="Izzatillo Khazratov",
    description="Online & batch prediction for model deployment",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "load-data=ICMD.data_loader:main",
            "start-server=ICMD.online.run_server:main",
            "run-inference-online=ICMD.online.run_inference:main",
            "schedule-batch-inference=ICMD.batch.schedule:main",
        ],
    },
    python_requires=">3.8",
)
