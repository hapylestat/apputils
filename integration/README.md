Steps to integrate AppUtils to the user application:
1) copy apputils_setup.py to your project root folder
2) modify setup.py as below: 
   - add new import: from apputils_setup import AppUtilsCommand
   - add new cmd class
    setup(
    ....
    cmdclass={
      ...
      "apputils": AppUtilsCommand
      ...
    }
    ....
    )
3) create the requirements file at the root folder: apputils-requirements.txt
  - first line is a relative path, where modules should be placed
  - following lines are list of modules to add to the project, module per line 

4) from the root folder execute: python3 setup.py apputils