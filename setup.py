from distutils.core import setup
setup(
    name='collection',         # How you named your package folder (MyLib)
    packages=['collection'],   # Chose the same as "name"
    package_dir={'collection': 'src/collection'},
    version='0.1.5',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='Laravel-style collection class that provides an interface for pipeline programming',
    author='Ryan Morton',                   # Type in your name
    author_email='thenerdscribe@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/thenerdscribe/collection',
    # I explain this later on
    download_url='https://github.com/thenerdscribe/collection/archive/0.1.5.tar.gz',
    # Keywords that define your package best
    keywords=['laravel', 'collection', 'pipeline'],
    install_requires=[            # I get to this in a second
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
