try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='muse',
    version='0.1',
    description='personal blogging engine',
    author='Faltzer (Chris Santiago)',
    author_email='faltzerr@aol.com',
    url='http://faltzershq.com/',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.5",
        "python-openid>=2.2.5",
        "SUIT>=2.0.1",
        "rulebox>=1.1.0",
        "lxml>=2.2.7",
        "FormEncode>=1.2.1",
        "recaptcha-client>=1.0.5"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'muse': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = muse.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)