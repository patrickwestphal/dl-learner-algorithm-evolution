import os
import pickle


class KnownCommitsStore(object):
    _pickle_file_path = '.known_commits.pickle'

    def __init__(self, pickle_file_path=None):
        if pickle_file_path:
            self._pickle_file_path = pickle_file_path

        if os.path.isfile(self._pickle_file_path):
            with open(self._pickle_file_path, 'rb') as f:
                self.commit_shas = pickle.load(f)

        else:
            self.commit_shas = []

    def __contains__(self, item):
        pass

    def append(self, commit_sha):
        self.commit_shas.append(commit_sha)

        with open(self._pickle_file_path, 'wb') as f:
            pickle.dump(self.commit_shas, f)
