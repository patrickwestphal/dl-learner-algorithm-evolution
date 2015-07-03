from .dllearnerrepo import DLLearnerRepo


def main():
    repo = DLLearnerRepo(repo_dir_path='/tmp/DLLearner', branch='master',
                         already_cloned=True)

    for commit in repo:
        commit.checkout()
        commit.build()
        print(commit.sha1)
        # break