from setuptools import find_packages, setup
import os


app_utils = __import__("apputils")
app_name = app_utils.__name__
app_author = app_utils.__author__
app_author_mail = app_utils.__author_mail__
app_ver = app_utils.__version__
app_url = app_utils.__url__


package_excludes = ("examples",)


README_PATH_MD = os.path.join(os.path.dirname(__file__), "README.md")
README_PATH_RST = os.path.join(os.path.dirname(__file__), "README.rst")

README_PATH = README_PATH_RST if os.path.exists(README_PATH_RST) else README_PATH_MD
print("Using {} for the description: ".format(os.path.basename(README_PATH)))

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
