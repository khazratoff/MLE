#!\usr\bin\python
"""Setuptools-based installation."""
import os
from pathlib import Path
from typing import List

from setuptools import find_packages, setup


readme = (Path(__file__).parent / 'README.md').read_text()


def get_dependencies() -> List[str]:
    with Path('requirements.txt').open() as file:
        dependencies = [line.rstrip() for line in file if not line.startswith('-') and '@git' not in line]
    return dependencies


setup(
    name='ICMD Project',
    version='0.0.1',
    author='Izzatillo Khazratov',
    description='Online & batch prediction for model deployment',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests', 'docs'],include=['src']),
    # include_package_data=True,
    install_requires=get_dependencies(),
    entry_points={
        'console_scripts': [
            'load-data=src.ICMD.data_loader:main',
            'start-server=src.ICMD.online.app:main',
            'run-inference-online=src.ICMD.online.run_inference:main',
            # 'run-inference-batch=src.titanic_project.batch.batch_pipeline:main',
        ],
    },
    python_requires='>3.8',
)