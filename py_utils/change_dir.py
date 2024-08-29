import os
from contextlib import contextmanager


@contextmanager
def change_dir(destination):
    try:
        cwd = os.getcwd()
        os.chdir(destination)
        yield
    finally:
        os.chdir(cwd)

if __name__ == "__main__":
    with change_dir('destination_dir'):
        print(os.listdir())