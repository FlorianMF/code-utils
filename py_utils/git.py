from logging import Logger
from pathlib import Path
from typing import Union

from git import InvalidGitRepositoryError, Repo

__all__ = [
    "get_repo_info",
]


def get_repo_info(repo_path: Union[str, Path]) -> dict[str, str]:
    """Parse repository information from path.

    Args:
        path (Union[pathlib.Path, str]): path to repo. If path is not a repository it
        searches parent folders for a repository

    Returns:
        dict: contains the current hash, gitdir and active branch
    """

    def find_repo(findpath):
        p = Path(findpath).absolute()
        for p in [p, *p.parents]:
            try:
                repo = Repo(p)
                break
            except InvalidGitRepositoryError:
                pass
        else:
            raise InvalidGitRepositoryError
        return repo

    repo = find_repo(repo_path)
    return {
        "hash": repo.head.commit.hexsha,
        "gitdir": repo.git_dir,
        "active_branch": repo.active_branch.name,
    }


