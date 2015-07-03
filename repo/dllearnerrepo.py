import codecs
import json
import os
import subprocess
import urllib.request

from collections import Iterator
from datetime import datetime
from datetime import timedelta
from git.repo import Repo


default_repo_dir_path = '/tmp/DL-Learner'
default_time_delta_in_days = 30
# the trailing slash is important!!!
components_core_dir = 'components-core/src/main/java/'


class DLLearnerRepo(Iterator):
    """
    TODO:
        - add progress bar
        - find out automatically whether the repo is already cloned and in case
          it is, just run a pull (after having set the branch)
        - handle branches
    """
    _commits_get_url = 'https://api.github.com/repos/AKSW/DL-Learner/commits' +\
                       '?per_page=10000&since=%s'
    _github_repo_url = 'https://github.com/AKSW/DL-Learner.git'

    def __init__(self, repo_dir_path=None, since=None, branch=None,
                 already_cloned=False):
        self.repo_dir_path = \
            default_repo_dir_path if not repo_dir_path else repo_dir_path

        if since is None:
            self.since = datetime.now() - timedelta(default_time_delta_in_days)
        else:
            self.since = since

        self.branch = branch
        self.commit_sha1s = None
        self.next_idx = None

        self._setup_repo(already_cloned)

    def _setup_repo(self, already_cloned):
        if already_cloned:
            self._git_repo = Repo(self.repo_dir_path)
        else:
            self._git_repo = Repo.clone_from(
                self._github_repo_url, self.repo_dir_path)

        if self.branch:
            self._git_repo.git.checkout(self.branch)
            # self._git_repo.active_branch = self.branch

    def __iter__(self):
        return self

    def __next__(self):
        if self.commit_sha1s is None:
            self.commit_sha1s = self._get_commits()
            self.next_idx = -1

        self.next_idx += 1
        if self.next_idx >= len(self.commit_sha1s):
            raise StopIteration

        return DLLearnerCommit(self.commit_sha1s[self.next_idx], self)

    def _get_commits(self):
        response = urllib.request.urlopen(self._commits_get_url % self.since.isoformat())
        encoder = codecs.getreader("utf-8")
        commits = json.load(encoder(response))

        return [cmmt['sha'] for cmmt in commits]

    def get_checkout_cmd(self):
        return self._git_repo.git.checkout


algorithms = {
    'AbstractCELA': {
        'score_method_str': 'getCurrentlyBestEvaluatedDescription().getAccuracy()'
    }
}


class DLLearnerCommit(object):
    """
    $ find . -name AbstractCELA.java
    $ sed -i '0,/import /s/import /import org.dllearner.core.AbstractCELA;\nimport /' ./interfaces/src/main/java/org/dllearner/cli/CLI.java
    $ sed -i 's/algorithm.start()/algorithm.start();System.out.println("+.+.+"+((AbstractCELA) algorithm).getCurrentlyBestDescription())/' ./interfaces/src/main/java/org/dllearner/cli/CLI.java
    $ cd interfaces/; mvn exec:java -Dexec.mainClass='org.dllearner.cli.CLI' -Dexec.args="../examples/father.conf"; cd - > /dev/null
    """
    output_marker_pattern = '-*-**-*-'
    class_to_cast_to = 'AbstractCELA'

    def __init__(self, sha1_string, repo):
        self.sha1 = sha1_string
        self.repo = repo
        self.checkout_cmd = repo.get_checkout_cmd()
        self.algorithm_class = 'AbstractCELA'

    def checkout(self):
        return self.checkout_cmd(self.sha1)

    def build(self):
        dirty_files = self._patch_repo()
        subprocess.check_call(['mvn', 'install', '-DskipTests=true'],
                              cwd=self.repo.repo_dir_path)

        output = subprocess.check_output(
            ['mvn', 'exec:java', '-Dexec.mainClass=org.dllearner.cli.CLI',
             '-Dexec.args=\'../examples/father.conf\''], cwd=self.repo.repo_dir_path + '/interfaces')

        output = output.decode('utf-8')
        acc = output.split(self.output_marker_pattern)[1]

        # import pdb; pdb.set_trace()
        print('##############################: ' + acc)
        with open('/tmp/res.txt', 'a') as f:
            f.write(acc + '\n')

        self._clean_repo(dirty_files)

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

        return [cli_file_path]

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
            raise RuntimeError('Should never happpen (TM) TODO: add useful error msg')

    def _clean_repo(self, dirty_files):
        for file in dirty_files:
            subprocess.check_call(['git', 'checkout', file], cwd=self.repo.repo_dir_path)
        pass