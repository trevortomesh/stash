from setuptools import setup

setup(
    name='stash-organizer',
    version='0.1.0',
    py_modules=['stash'],
    entry_points={
        'console_scripts': [
            'stash = stash:main',
        ],
    },
    author='Trevor Tomesh',
    author_email='tmtomesh@hotmail.com',
    description='A lightweight tool to sort and manage directory contents.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/stash',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)