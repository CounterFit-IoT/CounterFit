from setuptools import setup

setup(
    name='CounterFit',
    install_requires=[
        "Flask==2.1.2",
        "Flask-SocketIO==5.2.0",
        "eventlet==0.33.1",
        "beautifulsoup4==4.9.3",
        "lxml==4.6.4"
    ],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
