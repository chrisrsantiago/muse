# Copyright (c) 2010 Chris Santiago (http://faltzershq.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='muse',
    version='1.0',
    description='personal blogging engine',
    author='Faltzer (Chris Santiago)',
    author_email='faltzerr@aol.com',
    url='http://faltzershq.com/',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.6.3",
        "Elixir>=0.7.1",
        "python-openid>=2.2.5",
        "SUIT>=2.0.1",
        "rulebox>=1.1.0",
        "phanpy>=1.0.1",
        "FormEncode>=1.2.2",
        "recaptcha-client>=1.0.5"
    ],
    setup_requires=["PasteScript>=1.7.3"],
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