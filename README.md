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


# Execution

After the installation there should be available the executable `makestats`. The idea is to give this script

- the location where you want to store the cloned DL-Learner repo
- a DL-Learner config file which describes the learning setup
- a date from which on the statistics should be collected

The script then clones the repository into the target directory, gets all commits since the provided date, builds the DL-Learner for every commit, runs the setup described in the config file and collects the accuracy of the best learned concept.
In case you have already downloaded the DL-Learner and there is no need to clone it from GitHub you can indicate this by providing the `--localrepo` switch. If you want to refer to a certain branch 'xyz' you can use `--branch xyz`.
For the actual output of the results you can for example add `--plot /tmp/res.pdf` which will create a plot of the accuracy results over time. The actual file format is determined via the file suffix by the matplotlib.
For details just call `makestats -h`.
