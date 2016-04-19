from distutils.core import setup

setup(
    name='PlanOut',
    version='0.6.0',
    author='Facebook, Inc.',
    author_email='eytan@fb.com',
    packages=[
        'planout',
        'planout.ops',
        'planout.test'
    ],
    requires=[
        'six'
    ],
    url='http://pypi.python.org/pypi/PlanOut/',
    license='LICENSE',
    description='PlanOut is a framework for online field experimentation.',
    keywords=['experimentation', 'A/B testing'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Testing',
    ],
    long_description="""PlanOut is a framework for online field experimentation.
    PlanOut makes it easy to design both simple A/B tests and more complex
    experiments, including multi-factorial designs and within-subjects designs.
    It also includes advanced features, including built-in logging, experiment
    management, and serialization of experiments via a domain-specific language.
    """,
)

# long_description=open('README.md').read(),
