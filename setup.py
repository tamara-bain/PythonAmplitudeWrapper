from setuptools import setup

setup(
    name='Amplitude API Wrapper',
    version='0.82',
    url='https://github.com/tamara-bain/PythonAmplitudeWrapper',
    license='MIT',
    description='Python wrapper for amplitude api',
    install_requires=['django', 'djangorestframework', 'model-mommy'],

    py_modules=['amplitude_wrapper', 'requests'],
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