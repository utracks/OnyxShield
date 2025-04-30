from setuptools import setup, find_packages
from Cython.Build import cythonize
from setuptools.extension import Extension
import os

def build_extensions() -> list:
    return [
        Extension(
            "onyxshield.encrypt",
            sources=["onyxshield/encrypt.py"],
            extra_compile_args=[
                '-O3',
                '-fstack-protector-strong',
                '-D_FORTIFY_SOURCE=2'
            ]
        )
    ]

setup(
    name="onyxshield",
    version="2.5.0",
    packages=find_packages(),
    ext_modules=cythonize(
        build_extensions(),
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'initializedcheck': False,
            'cdivision': True
        }
    ),
    install_requires=[
        'Cython>=0.29.24',
        'pycryptodome>=3.10.1'
    ],
    entry_points={
        'console_scripts': [
            'onyxshield=onyxshield.cli:main',
        ],
    },
    python_requires=">=3.7",
)