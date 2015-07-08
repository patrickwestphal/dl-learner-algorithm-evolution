import codecs
import json
import logging
import os
import subprocess
import urllib.request

from collections import Iterator
from datetime import datetime
from datetime import timedelta
from git.repo import Repo


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
_log = logging.getLogger()


default_time_delta_in_days = 30
# the trailing slash is important!!!
components_core_dir = 'components-core/src/main/java/'


class DLLearnerRepo(Iterator):
    """
    TODO:
        - add progress bar for repo download
        - find out automatically whether the repo is already cloned and in case
          it is, just run a pull (after having set the branch)
    """
    _commits_get_url = 'https://api.github.com/repos/AKSW/DL-Learner/commits' +\
                       '?per_page=10000&since=%s&sha=%s'
    _github_repo_url = 'https://github.com/AKSW/DL-Learner.git'

    def __init__(self, repo_dir_path, since=None, branch='develop',
                 already_cloned=False):
        self.repo_dir_path = repo_dir_path

        if since is None:
            self.since = datetime.now() - timedelta(default_time_delta_in_days)
        else:
            self.since = since

        self.branch = branch
        self.commit_sha1s = None
        self.next_idx = None

        self._setup_repo(already_cloned)

    def __len__(self):
        if self.commit_sha1s is None:
            self._init_commit_sha1s()

        return len(self.commit_sha1s)

    def _setup_repo(self, already_cloned):
        if already_cloned:
            self._git_repo = Repo(self.repo_dir_path)
        else:
            _log.info('Cloning repo from %s into %s' % (
                self._github_repo_url, self.repo_dir_path))
            self._git_repo = Repo.clone_from(
                self._github_repo_url, self.repo_dir_path)
            _log.info('-Done-')

        if self.branch:
            self._git_repo.git.checkout(self.branch)
            # self._git_repo.active_branch = self.branch

    def __iter__(self):
        return self

    def __next__(self):
        if self.commit_sha1s is None:
            self._init_commit_sha1s()

        self.next_idx += 1
        if self.next_idx >= len(self.commit_sha1s):
            raise StopIteration

        return DLLearnerCommit(self.commit_sha1s[self.next_idx], self)

    def _init_commit_sha1s(self):
        self.commit_sha1s = self._get_commits()
        self.next_idx = -1

    def _get_commits(self):
        response = urllib.request.urlopen(
            self._commits_get_url % (self.since.isoformat(), self.branch))

        encoder = codecs.getreader("utf-8")
        commits = json.load(encoder(response))

        return [cmmt['sha'] for cmmt in commits]

    def get_checkout_cmd(self):
        return self._git_repo.git.checkout


algorithms = {
    'AbstractCELA': {
        'score_method_str':
            'getCurrentlyBestEvaluatedDescription().getAccuracy()'
    }
}


class AlgorithmExecutionError(Exception):
    pass


class DLLearnerCommit(object):
    """
    My command line trials:
    $ find . -name AbstractCELA.java
    $ sed -i '0,/import /s/import /import org.dllearner.core.AbstractCELA;\nimport /' ./interfaces/src/main/java/org/dllearner/cli/CLI.java
    $ sed -i 's/algorithm.start()/algorithm.start();System.out.println("+.+.+"+((AbstractCELA) algorithm).getCurrentlyBestDescription())/' ./interfaces/src/main/java/org/dllearner/cli/CLI.java
    $ cd interfaces/; mvn exec:java -Dexec.mainClass='org.dllearner.cli.CLI' -Dexec.args="../examples/father.conf"; cd - > /dev/null
    """
    output_marker_pattern = '-*-**-*-'
    # TODO: make this configurable
    class_to_cast_to = 'AbstractCELA'

    def __init__(self, sha1_string, repo):
        self.sha1 = sha1_string
        self.repo = repo
        self.checkout_cmd = repo.get_checkout_cmd()
        self.algorithm_class = 'AbstractCELA'
        self._dirty_files = []

    def checkout(self):
        return self.checkout_cmd(self.sha1)

    def build(self):
        _log.info('Building repo for commit %s' % self.sha1)
        self._patch_repo()
        subprocess.check_call(['mvn', 'install', '-DskipTests=true'],
                              cwd=self.repo.repo_dir_path,
                              stdout=open(os.devnull, 'w'))
        _log.info('-Done-')

    def run(self, path_to_config_file):
        _log.info('Running learning setup for commit %s' % self.sha1)
        output = subprocess.check_output(
            ['mvn', 'exec:java', '-Dexec.mainClass=org.dllearner.cli.CLI',
             '-Dexec.args=\'' + path_to_config_file + '\''],
            cwd=self.repo.repo_dir_path + '/interfaces')

        output = output.decode('utf-8')
        output_parts = output.split(self.output_marker_pattern)

        if len(output_parts) > 1:
            acc = output_parts[1]
        else:
            raise AlgorithmExecutionError()

        acc = float(acc)

        _log.info('-Done-')
        return acc

    def clean_up(self):
        _log.info('Cleaning up repo for commit %s' % self.sha1)
        for file in self._dirty_files:
            subprocess.check_call(['git', 'checkout', file],
                                  cwd=self.repo.repo_dir_path)
        _log.info('-Done-')

    def _patch_repo(self):
        java_file_path = self._find_java_file(self.algorithm_class)
        cli_file_path = self._find_java_file('CLI')

        # add import statement
        import_statement = self._build_imprt_stmnt(java_file_path)

        sed_replace_str = '0,/import /s/' \
                          'import /' +\
                          import_statement + ';\\nimport /'
        subprocess.check_call(['sed', '-i', sed_replace_str, cli_file_path])

        # add print statement
        sed_replace_str = \
            's/algorithm.start()/' \
            'algorithm.start(); System.out.println("' + \
            self.output_marker_pattern + '" + ' \
            '((' + self.algorithm_class + ') algorithm).' + \
            algorithms[self.algorithm_class]['score_method_str'] + \
            ' + "' + self.output_marker_pattern + '")/'
        subprocess.check_call(['sed', '-i', sed_replace_str, cli_file_path])

        self._dirty_files.append(cli_file_path)

    def _find_java_file(self, algorithm_name):
        file_name = algorithm_name + '.java'

        res = subprocess.check_output(
            ['find', self.repo.repo_dir_path, '-name', file_name])

        return res.split(b'\n')[0].decode('utf-8')

    def _build_imprt_stmnt(self, file_path):
        if file_path.startswith(self.repo.repo_dir_path):
            tmp = file_path[len(self.repo.repo_dir_path):]
            comp_core_path_len = len(os.path.sep + components_core_dir)
            tmp = tmp[comp_core_path_len:]

            tmp = tmp.replace('.java', '')
            tmp = tmp.replace(os.path.sep, '.')

            return 'import ' + tmp

        else:
            raise RuntimeError(
                'Java file %s outside the repository directory %s!!!' % (
                    file_path, self.repo.repo_dir_path))
