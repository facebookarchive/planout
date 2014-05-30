from distutils.core import setup

setup(
    name='PlanOut',
    version='0.2.2',
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
    long_description="""PlanOut is a framework for online field experimentation.
    PlanOut makes it easy to design both simple A/B tests and more complex
    experiments, including multi-factorial designs and within-subjects designs.
    It also includes advanced features, including built-in logging, experiment
    management, and serialization of experiments via a domain-specific language.
    """,
)

#long_description=open('README.md').read(),
