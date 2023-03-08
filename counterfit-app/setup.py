from setuptools import setup

setup(
    name='CounterFit',
    install_requires=[
        "Flask==2.1.2",
        "Flask-SocketIO==5.2.0",
        "eventlet==0.33.3"
    ],
    tests_require=['pytest==7.2.2'],
    test_suite='tests',
)
