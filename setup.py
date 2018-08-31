"""
TimeUUID
-------------
Sequentially sortable, time-based UUIDs
"""

from setuptools import setup

setup(
    name='Amplitude API Wrapper',
    version='0.2',
    url='https://github.com/tamara-bain/PythonAmplitudeWrapper',
    license='MIT',
    description='Python wrapper for amplitude api',

    py_modules=['amplitude_wrapper'],
    platforms='any',
    test_suite='test_amplitude_wrapper',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)