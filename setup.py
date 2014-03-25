from distutils.core import setup

setup(
    name='PlanOut',
    version='0.1.0',
    author='Facebook, Inc.',
    author_email='planout@fb.com',
    packages=[
        'planout', 
        'planout.ops', 
        'planout.test'
    ],
    url='http://pypi.python.org/pypi/PlanOut/',
    license='LICENSE',
    description='PlanOut is a framework for online field experimentation.',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
