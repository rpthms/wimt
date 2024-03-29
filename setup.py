from setuptools import setup

setup(
    name='wimt',
    version='0.1',
    description='Where is my train?',
    url='https://github.com/rpthms/wimt',
    author='Ronnie P. Thomas',
    author_email='ronnietom@gmail.com',
    license='MIT',

    packages=['wimt'],
    include_package_data=True,

    # Required packages
    install_requires=['requests', 'lxml', 'jinja2'],
    python_requires='>=3',

    # Entry point
    entry_points={
        'console_scripts': [
            'wimt = wimt.__main__:main'
        ]
    }
)
