from setuptools import find_packages, setup

core_module = __import__("apputils.core").core
app_name = core_module.__name__
app_author = core_module.__author__
app_author_mail = core_module.__author_mail__
app_ver = core_module.__version__
app_url = core_module.__url__


package_excludes = ("examples",)

setup(
  name=app_name,
  version=app_ver,
  url=app_url,
  author=app_author,
  author_email=app_author_mail,
  description='Application modules swiss-knife',
  license='lGPL v3',
  zip_safe=False,
  packages=find_packages(exclude=package_excludes),

  include_package_data=True,
  classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ],
)
