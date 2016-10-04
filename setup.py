from setuptools import find_packages, setup

VERSION = '0.0.1'

setup(
    name='wordpad_glitch',
    version=VERSION,
    description='A wordpad glitch emulator',
    long_description=open('README').read(),
    url='https://github.com/justinfay/batch_wordpad_glitch',
    license='MIT',
    keywords='glitch art',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'wordpadglitch = wordpad_glitch:parse_args'],
    })
