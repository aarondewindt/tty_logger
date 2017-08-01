from setuptools import setup, find_packages
from distutils.util import convert_path


main_ns = {}
ver_path = convert_path('xsens_logger/__init__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='xsens_logger',
    version=main_ns['__version__'],
    description='Xsens logger',
    author='Aaron de Windt',
    author_email='',
    url='https://github.com/aarondewindt/xsens_logger',
    install_requires=['pyserial'],
    packages=find_packages('.', exclude=["test"]),
    entry_points={
          'console_scripts': [
              'start = xsens_logger.__main__:main'
          ]
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 2 - Pre-Alpha'],
)
