from setuptools import setup, find_packages

setup(
    name='glu',
    packages=find_packages(),
    url='https://github.com/chongkong/glu',
    license='MIT',
    version='0.0.18',
    description='Glue for DRY configurations',
    author='Park Jong Bin',
    author_email='chongkong94@gmail.com',
    keywords=['glue', 'glu', 'dry', 'config', 'dry-config', 'dry-configurable'],
    zip_safe=False,
    install_requires=[
        'future==0.15.2',
        'PyYAML==3.11'
    ],
    entry_points={
        'console_scripts': [
            'glu = glu.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
