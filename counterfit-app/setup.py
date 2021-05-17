from setuptools import setup

setup(
    name='CounterFit',
    install_requires=[
        "Flask==1.1.2",
        "Flask-SocketIO==5.0.1",
        "eventlet==0.30.2",
        "beautifulsoup4==4.9.3",
        "lxml==4.6.3"
    ],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
