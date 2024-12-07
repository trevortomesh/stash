from setuptools import setup, find_packages

setup(
    name='stash',
    version='1.0.0',
    description='A Python-based directory sorting tool',
    author='Your Name',
    author_email='youremail@example.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'stash=stash.stash:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
