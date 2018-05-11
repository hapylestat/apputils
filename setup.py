from setuptools import find_packages, setup
import os


core_module = __import__("apputils")
app_name = core_module.__name__
app_author = core_module.__author__
app_author_mail = core_module.__author_mail__
app_ver = core_module.__version__
app_url = core_module.__url__


package_excludes = ("examples",)


README_PATH = os.path.join(os.path.dirname(__file__), "README.md")

with open(README_PATH, "r") as f:
  readme_content = f.read()

setup(
  name=app_name,
  version=app_ver,
  url=app_url,
  author=app_author,
  author_email=app_author_mail,
  description='Application modules swiss-knife',
  long_description=readme_content,
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
    'Programming Language :: Python :: 3.6'
  ],
)
