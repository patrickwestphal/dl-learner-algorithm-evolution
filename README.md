Collection of scripts that show the performance evolution of DL-Learner algrothms

# Installation

The standard installation procedure would simply require to clone this repository, `cd` into it and use `pip` to install it like so:

```
$ git clone https://github.com/patrickwestphal/dl-learner-regression-stats.git
$ cd dl-learner-regression-stats/
# pip install .
```

Since the project uses Python packages like numpy that need to be compiled make sure you have the Python header files installed (python3-dev on Debian based systems). It might also be the case that you run into [this](http://stackoverflow.com/questions/27024731/matplotlib-compilation-error-typeerror-unorderable-types-str-int)   error which would also require installing libfreetype-dev.
Note that the actual `pip install` call requires root priviliges and will install Python packages into your system. Although this can be undone via `pip uninstall dl-learner-regression-stats` the recommended way is to use virtualenv as briefly described in the next section.
