from setuptools import find_packages, setup
import os


# versioning  https://www.python.org/dev/peps/pep-0440/

def get_version():
  app_version_module = __import__("apputils.version").version
  app_ver = app_version_module.__version__

  build_number = os.environ['TRAVIS_BUILD_NUMBER'] if 'TRAVIS_BUILD_NUMBER' in os.environ else '0'
  commit_msg = os.environ['COMMIT_MSG'] if 'COMMIT_MSG' in os.environ else None

  if 'GIT_BRANCH' in os.environ and os.environ['GIT_BRANCH'] == "master":
    app_ver = f"{app_ver}dev{build_number}"
  elif commit_msg and '[RC]' in commit_msg:
    app_ver = f"{app_ver}rc{build_number}"
  elif 'GIT_BRANCH' in os.environ and os.environ['GIT_BRANCH'] == "testing":
    app_ver = f"{app_ver}b{build_number}"
  elif 'GIT_BRANCH' in os.environ and os.environ['GIT_BRANCH'] == "production":
    app_ver = f"{app_ver}.{build_number}"

  return app_ver


def get_long_description():
  readme_path = os.path.join(os.path.dirname(__file__), "README.md")

  try:
    with open(readme_path, "r") as f:
      readme_content = f.read()
  except FileNotFoundError:
    readme_content = ""

  return readme_content


app_utils = __import__("apputils")
app_name = app_utils.__name__
app_author = app_utils.__author__
app_author_mail = app_utils.__author_mail__
app_version = get_version()
app_url = app_utils.__url__


package_excludes = {"examples", "tests"}


setup(
  name=app_name,
  version=app_version,
  url=app_url,
  author=app_author,
  author_email=app_author_mail,
  description='Application modules swiss-knife',
  long_description=get_long_description(),
  long_description_content_type='text/markdown',
  license='lGPL v3',
  zip_safe=False,
  packages=find_packages(exclude=package_excludes),

  include_package_data=True,
  classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6'
  ],
)
