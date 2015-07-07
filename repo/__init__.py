from subprocess import CalledProcessError
import datetime
import logging

import numpy as np

from .dllearnerrepo import AlgorithmExecutionError
from .dllearnerrepo import DLLearnerRepo


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
_log = logging.getLogger()


def main():
    """
    TODO:
     - log overview of what is to be done (repo dir; get commits since when...)
    """
    repo = DLLearnerRepo(repo_dir_path='/tmp/DLLearnerMstr',
                         since=datetime.datetime(2015, 3, 1),
                         branch='master',
                         already_cloned=False)

    accuracies = np.zeros((len(repo), 1), dtype=np.float16)
    accuracies[accuracies==0] = np.nan
    commits = []
    cmmt_cntr = 0

    for commit in repo:
        _log.info('--- Running learning setup with commit %s (%i/%i)---' % (
            commit.sha1, cmmt_cntr, len(repo)))
        commits.append(commit.sha1)

        # TODO: handle build errors
        try:
            commit.checkout()
            commit.build()
            # acc = commit.run('/tmp/DLLearner/examples/father.conf')
            acc = commit.run('/tmp/param.conf')
            _log.info('--- Got accuracy of %f ---' % acc)
            accuracies[cmmt_cntr] = acc

        except (CalledProcessError, AlgorithmExecutionError) as e:
            _log.error(e)

        commit.clean_up()
        cmmt_cntr += 1

    return accuracies, commits
