"""
Python client module for GGMP, the Generic Gameserver Messaging Protocol
"""
from setuptools import find_packages, setup

dependencies = []

setup(
    name='ggmp-client',
    version='0.2.0',
    url='https://github.com/bomattin/ggmp-client',
    download_url='https://github.com/ggmpteam/ggmp-client-py/tarball/0.2.0',
    license='BSD',
    author='Bret Mattingly 2',
    author_email='bret.mattingly@gmail.com',
    description='Python client module for GGMP, the Generic Gameserver Messaging Protocol',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={},
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        # 'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Windows',
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)