from setuptools import setup

version = '0.1'

requirements = [
    'requests',
    'python-dateutil',
    'halo',
]


setup(
    name='gttr',
    version=version,
    packages=[
        'gttr',
        'gttr.lib',
    ],
    url='https://github.com/a1fred/gttr',
    entry_points={
        'console_scripts': ['gttr=gttr.cli:cli'],
    },
    license='MIT',
    author='a1fred',
    author_email='demalf@gmail.com',
    description='GitLab time tracking tool',
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=requirements,
    test_suite="tests",
)
