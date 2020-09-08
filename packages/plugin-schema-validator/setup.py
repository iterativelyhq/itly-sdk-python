from setuptools import setup

setup(
    name='itly.plugin-schema-validator',
    version='0.0.11',
    description='Iteratively Analytics SDK - Schema Validator Plugin',
    long_description='Iteratively Analytics SDK - Schema Validator Plugin',
    url='https://github.com/iterativelyhq/itly-sdk-python',
    author='Iteratively',
    license='MIT',
    packages=['itly.plugin_schema_validator'],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires=">3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4",
    install_requires=[
        'jsonschema',
        'itly.sdk',
    ],
)
