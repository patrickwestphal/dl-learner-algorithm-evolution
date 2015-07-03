import unittest

from datetime import datetime

from repo.dllearnerrepo import DLLearnerRepo


def dummy(*args):
    pass


class DLLearnerRepoTests(unittest.TestCase):

    def setUp(self):
        # skip the actual setup of the git repo which would require internet
        # access and an existing path in the file system
        self._setup_repo_fn = DLLearnerRepo._setup_repo
        DLLearnerRepo._setup_repo = dummy

    def tearDown(self):
        DLLearnerRepo._setup_repo = self._setup_repo_fn

    def test___init__01(self):
        repo = DLLearnerRepo()
        self.assertTrue(len(repo.repo_dir_path) > 0)
        self.assertTrue(isinstance(repo.since, datetime))
        self.assertIsNone(repo.branch)

    def test__init__02(self):
        repo_dir_path = '/tmp/foo'
        since = datetime(2023, 5, 23)
        branch = 'branchxyz'
        repo = DLLearnerRepo(repo_dir_path, since, branch)

        self.assertEqual(repo_dir_path, repo.repo_dir_path)
        self.assertEqual(since, repo.since)
        self.assertEqual(branch, repo.branch)
