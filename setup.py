#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
#   Author(s): Milan Falesnik   <milan@falesnik.net>
#                               <mfalesni@redhat.com>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from setuptools import setup


setup(
    name="Beheaded",
    version="1.2",
    author="Milan Falešník",
    author_email="milan@falesnik.net",
    description="Generic X window and recording for headless setups in Python.",
    license="GPLv2",
    keywords="headless xvfb ffmpeg recording",
    url="https://github.com/mfalesni/Beheaded",
    packages=["Beheaded"],
    install_requires=['Runner>=1.1'],
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording"
    ]
)
