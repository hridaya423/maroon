from setuptools import setup, find_packages

setup(
    name='maroon',
    version='0.1.0',
    packages=find_packages(),
    description='A pirate-themed programming language interpreter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Hridya Agrawal',
    author_email='hridayahoney@gmail.com',
    url='https://github.com/hridaya423/maroon',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'maroon=src.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
)