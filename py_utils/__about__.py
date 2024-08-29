from datetime import date

__version__ = "0.1.0"

__package_name__ = "python-utils"
__author_name__ = "FlorianMF"
__author_email__ = "florian.mueller.fouarge@gmail.com"
# __maintainer_name__ = 'MAINTAINER_NAME'
# __maintainer_email__ = 'MAINTAINER_EMAIL'
__license__ = "LICENSE"
__copyright__ = f"Copyright (c) 2020-{date.today().year}, {__author_name__}."
__homepage__ = "https://github.com/FlorianMF/python-utils"
__download_url__ = "https://github.com/FlorianMF/python-utils"
# this has to be simple string, see: https://github.com/pypa/twine/issues/522
__docs__ = "PACKAGE_DESCRIPTION"
__long_docs__ = """
What is it?
-----------
Describe the package

Second title
----------------
Description

Another title
------------------
Description
"""

__all__ = [
    "__version__",
    "__package_name__",
    "__author_name__",
    "__author_email__",
    "__license__",
    "__copyright__",
    "__homepage__",
    "__download_url__",
    "__docs__",
    "__long_docs__",
]