try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="email_me_when_ready",
    version='0.0.7',
    description="A decorator that can be wrapped around any function and will send you an email from your gmail when the function has run its course.",
    author='Adam Bannister',
    author_email='adam.p.bannister@gmail.com',
    package_dir={'email_me_when_ready': 'email_me_when_ready'},
    include_package_data=True,
    packages = ['email_me_when_ready'],
)
