#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is used to create the package we'll publish to PyPI.

.. currentmodule:: setup.py
.. moduleauthor:: Alper Ozaydin <alperozaydinn@gmail.com>
"""

import importlib.util
import os
from pathlib import Path
from typing import List
from setuptools import setup, find_packages

# Get the base version from the library.  (We'll find it in the `version.py`
# file in the src directory, but we'll bypass actually loading up the library.)
vspec = importlib.util.spec_from_file_location(
    "version", str(Path(__file__).resolve().parent / "trade_plate" / "version.py")
)
vmod = importlib.util.module_from_spec(vspec)
vspec.loader.exec_module(vmod)
version = getattr(vmod, "__version__")

# If the environment has a build number set...
if os.getenv("buildnum") is not None:
    # ...append it to the version.
    version = f"{version}.{os.getenv('buildnum')}"


def install_requires() -> List[str]:
    from pkg_resources import parse_requirements

    with Path("requirements.txt").open() as f:
        return [str(requirement) for requirement in parse_requirements(f)]


setup(
    name="trade-plate",
    description="Crypto trading tool",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    install_requires=[install_requires()],
    entry_points="""
    [console_scripts]
    trade-plate=trade_plate.cli:cli
    """,
    python_requires=">=0.0.1",
    license=None,  # noqa
    author="Alper Ozaydin",
    author_email="alperozaydinn@gmail.com",
    # Use the URL to the github repo.
    url="https://github.com/alperozaydin/trade_plate",
    download_url=(
        f"https://github.com/alperozaydin/" f"trade_plate/archive/{version}.tar.gz"
    ),
    keywords=[
        # Add package keywords here.
    ],
    # See https://PyPI.python.org/PyPI?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for.
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        # Pick your license.  (It should match "license" above.)
        """License :: OSI Approved :: <Your Preferred License>""",  # noqa
        # noqa
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
)
