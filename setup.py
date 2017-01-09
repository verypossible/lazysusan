from setuptools import setup, find_packages

setup(
    name='lazysusan',
    packages=find_packages(exclude=[
        'docs', 'docs.*',
        'examples', 'examples.*',
        'tests', 'tests.*',
    ]),
    version = '0.7',
    description = 'A library for authoring Alexa apps',
    author='Spartan Systems',
    author_email='sass@joinspartan.com',
    url='https://github.com/spartansystems/lazysusan',
    install_requires=[
        'PyYAML==3.12',
        'boto3==1.4.1',
    ],
    tests_require=[
        'pytest>=3.0.4',
        'pytest-cov>=2.4.0',
        'pytest-mock>=1.5.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
    ]
)

