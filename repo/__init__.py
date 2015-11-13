from subprocess import CalledProcessError
import logging

from .dllearnerrepo import AlgorithmExecutionError
from .dllearnerrepo import DLLearnerRepo


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
_log = logging.getLogger()


def main(repo_dir_path, config_file_path, since, branch='develop',
         already_cloned=False):
    """
    TODO:
     - log overview of what is to be done (repo dir; get commits since when...)
     - use tmp directory
    """
    repo = DLLearnerRepo(repo_dir_path=repo_dir_path, since=since,
                         branch=branch, already_cloned=already_cloned)

    commits = []
    res = []
    cmmt_cntr = 1

    for commit in repo:
        _log.info('--- Running learning setup with commit %s (%i/%i)---' % (
            commit.sha1, cmmt_cntr, len(repo)))
        commits.append(commit.sha1)

        try:
            commit.checkout()
            commit.build()
            vals = commit.run(config_file_path)
            _log.info('--- Got %s ---' % str(vals))
            res.append(vals)

        except (CalledProcessError, AlgorithmExecutionError) as e:
            res.append([])
            _log.error(e)

        commit.clean_up()
        cmmt_cntr += 1

    return res, commits
