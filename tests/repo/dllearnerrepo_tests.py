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
        repo = DLLearnerRepo('/tmp/foo')
        self.assertTrue(len(repo.repo_dir_path) > 0)
        self.assertTrue(isinstance(repo.since, datetime))
        self.assertEquals('develop', repo.branch)

    def test__init__02(self):
        repo_dir_path = '/tmp/foo/'
        stripped_repo_dir_path = '/tmp/foo'
        since = datetime(2023, 5, 23)
        branch = 'branchxyz'
        repo = DLLearnerRepo(repo_dir_path, since, branch)

        self.assertEqual(stripped_repo_dir_path, repo.repo_dir_path)
        self.assertEqual(since, repo.since)
        self.assertEqual(branch, repo.branch)

    def test___len__(self):
        repo = DLLearnerRepo('/tmp/foo')
        repo.commit_sha1s = [
            '8f6c2b905727510cbf113f8bc4f9cec6d6702270',  # 01
            '8a37dee6555496195dda0d15d434c5b434f07e92',  # 02
            '22c03520d6e9d459be57cd16060bbdda12062cc6',  # 03
            'fcd4d3bce964b692e154d43835e52851afcf2e66',  # 04
            '5dd975f04af009d4e80be7433888075a664ce24e',  # 05
            'c498fde1038940e22e307fe9263824627675e26b',  # 06
            'f153bbcbfa6abaa26a73b0ee7476bb6550522c97',  # 07
            '8247d83103d7081a37d692388254dfac95d1800c',  # 08
            '001006f9239f38b6010bd38c1533b5596fd1a79f',  # 09
            '3badd9b68a51b7eb03261e9bd17831e243e169b3',  # 10
            '3ce56045d009f9b986a8c27f245e1b91b2849d6e'   # 11
        ]
        self.assertEquals(11, len(repo))

