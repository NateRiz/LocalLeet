import setuptools

setuptools.setup(
name="Localleet",
version='1.0.0',
description="Local Leetcode Problems",
long_description="LocalLeet is a command line interface for retrieval and submission of problems from https://leetcode.com/.",
url="https://github.com/NateRiz/LocalLeet",
author="Nathan Rizik",
author_email="nathan.rizik@gmail.com",
license="GNU GPLv3",
classifiers = [
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
keywords ="leetcode local algorithm interview selenium terminal",
packages=setuptools.find_packages(),
install_requires=["selenium", "chromedriver_installer"],
entry_points={'console_scripts': ['leet=LocalLeet.localleet:main']}
)
