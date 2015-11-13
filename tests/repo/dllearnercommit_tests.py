import unittest

from repo import DLLearnerCommit, DLLearnerRepo


def dummy(*args):
    pass


def dummy_checkout_cmd(sha1):
    return sha1


def dummy_get_checkout_cmd(*args):
    return dummy_checkout_cmd


class DLLearnerCommitTests(unittest.TestCase):

    def setUp(self):
        DLLearnerRepo.get_checkout_cmd = dummy_get_checkout_cmd

        # skip the actual setup of the git repo which would require internet
        # access and an existing path in the file system
        self._setup_repo_fn = DLLearnerRepo._setup_repo
        DLLearnerRepo._setup_repo = dummy

    def test___init__(self):
        sha1 = 'c498fde1038940e22e307fe9263824627675e26b'
        repo = DLLearnerRepo('/tmp/foo')
        commit = DLLearnerCommit(sha1, repo)

        self.assertEquals(sha1, commit.sha1)
        self.assertEquals(repo, commit.repo)
        self.assertEquals(dummy_checkout_cmd, commit.checkout_cmd)
        self.assertTrue(isinstance(commit.algorithm_setup, str))
        self.assertEqual(0, len(commit._dirty_files))

    def test_checkout(self):
        sha1 = 'c498fde1038940e22e307fe9263824627675e26b'
        repo = DLLearnerRepo('/tmp/foo')
        commit = DLLearnerCommit(sha1, repo)

        self.assertEqual(sha1, commit.checkout())

    def test_build_imprt_stmnt(self):
        sha1 = 'c498fde1038940e22e307fe9263824627675e26b'
        repo = DLLearnerRepo('/tmp/foo')
        commit = DLLearnerCommit(sha1, repo)
        file_path = '/tmp/foo/components-core/src/main/java/foo/bar/Baz.java'
        expected_import_str = 'import foo.bar.Baz'

        import_str = commit._build_imprt_stmnt(file_path)
        self.assertEquals(expected_import_str, import_str)
