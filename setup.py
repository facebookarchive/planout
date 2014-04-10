from distutils.core import setup

setup(
    name='PlanOut',
    version='0.1.1',
    author='Facebook, Inc.',
    author_email='eytan@fb.com',
    packages=[
        'planout', 
        'planout.ops', 
        'planout.test'
    ],
    url='http://pypi.python.org/pypi/PlanOut/',
    license='LICENSE',
    description='PlanOut is a framework for online field experimentation.',
    keywords=['experimentation', 'A/B testing'],
    long_description=open('README.md').read(),
)
