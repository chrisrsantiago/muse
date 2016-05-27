# Copyright (c) 2010 Chris Santiago (http://faltzershq.com/)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
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
try:
    from babel.messages import frontend as babel
except ImportError:
    print 'The Babel package is not installed; to install, run:'
    print 'easy_install babel'
    exit()

setup(
    name='muse',
    version='1.0',
    description='personal blogging engine',
    author='Faltzer',
    author_email='chrisrsantiago@aol.com',
    url='http://github.com/chrisrsantiago/muse',
    install_requires=[
        'Pylons>=1.0',
        'SQLAlchemy>=0.6.3',
        'python-openid>=2.2.5',
        'SUIT>=2.0.1',
        'rulebox>=1.1.0',
        'phanpy>=1.1.0',
        'FormEncode>=1.2.2',
        'pygeoip>=0.1.3',
        'recaptcha-client>=1.0.5',
        'whoosh>=1.0.0b11'
    ],
    setup_requires=['PasteScript>=1.7.3'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    cmdclass={
        'compile_catalog': babel.compile_catalog,
        'extract_messages': babel.extract_messages,
        'init_catalog': babel.init_catalog,
        'update_catalog': babel.update_catalog
    },
    message_extractors = {
        'muse': [
            ('**.py', 'python', None),
            ('templates/**.tpl', 'suit', None),
            ('public/**', 'ignore', None)
        ]
    },
    package_data={'muse': ['i18n/*/LC_MESSAGES/*']},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points='''
    [paste.app_factory]
    main = muse.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    ''',
)