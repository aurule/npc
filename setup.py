from setuptools import setup, find_packages
from codecs import open
from os import path

with open('npc/__version__.py') as ver:
    exec(ver.read())

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='npc',
    version=__version__,
    description="Game master's tool to manage characters and other campaign files",
    long_description=long_description,
    url="https://github.com/aurule/npc",
    author="Peter Andrews",
    author_email="pmandrews@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="npc tabletop gaming gm campaign",
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "Mako>=1.0.6",
        "Markdown>=2.6.7",
        "PyQt5>=5.7.1"
    ],
    extras_require={
        "test": [
            "pytest>=3.0.6",
            "pytest-qt>=2.1.0"
        ]
    },
    package_data={
        'npc.settings': ['settings-default.json', 'settings-changeling.json']
    },
    entry_points={
        'console_scripts': [
            'npc=npc.cli:start',
            'npc-gui=npc.gui:start',
        ]
    }
)
