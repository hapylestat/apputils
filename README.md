# appcore  [![Build Status](https://travis-ci.org/hapylestat/apputils.svg?branch=master)](https://travis-ci.org/hapylestat/apputils) [![Documentation Status](https://readthedocs.org/projects/appcore/badge/?version=latest)](http://appcore.readthedocs.io/en/latest/?badge=latest)
Core modules for python application.

Provides possibility to:
- Working with configuration file
- Split one configuration file, to several (via modules feature)
- Change any configuration item from command line
- Working "In Memory" mode, without parsing configuration
- Logging


Even more come !


# How to connect to your Project

pip install git+https://github.com/hapylestat/appcore.git

# How to use

test.py
```
from appcore.core import config


def main():
   conf = config.get_instance(in_memory=True)
   print(conf.get("main.arg", check_type=str, default="main argument"))

if __name__ == "__main__":
    main()

```

Console:
```
# python test.py main.arg=test
test
```
