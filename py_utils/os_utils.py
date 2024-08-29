import os

USER_PATH = os.path.expanduser('~')
DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
DOCUMENTS_PATH = os.path.join(os.path.expanduser('~'), 'Documents')

_check_funcs = {
    'any': any,
    'all': all,
}


def list_directory(directory, strings_to_contain=[''], mode='any'):
    """Returns all file and folders in the directory which contain the demanded strings.

    Parameters
    ----------
    directory : str
        path of the directory

    strings_to_contain : (str, list)
        strings which the folder and file names need to contain,
        by default ['']

    mode : str, optional
        'any' - only one element of 'strings_to_contain' has to be present
        'all' - all elements of 'strings_to_contain' have to be present,
            by default 'any'

    Returns
    -------
    list
        list of the paths of the files and folders in the directory which follow the requirements.
    """

    if isinstance(strings_to_contain, str):
        strings_to_contain = [strings_to_contain]
    function = _check_funcs[mode]
    return [os.path.join(directory, f) for f in os.listdir(directory)
            if function(x in f for x in strings_to_contain)]


def list_folders(directory, strings_to_contain=[''], mode='any'):
    """Returns all folders in the directory which contain the demanded strings.

    Parameters
    ----------
    directory : str
        path of the directory

    strings_to_contain : (str, list)
        strings which the folder and file names need to contain,
        by default ['']

    mode : str, optional
        'any' - only one element of 'strings_to_contain' has to be present
        'all' - all elements of 'strings_to_contain' have to be present,
            by default 'any'

    Returns
    -------
    list
        list of the paths of the folders in the directory which follow the requirements.
    """
    dir_list = list_directory(directory, strings_to_contain, mode)

    return [f for f in dir_list if os.path.isdir(f)]


def list_files(directory, strings_to_contain=[''], mode='any'):
    """Returns all folders in the directory which contain the demanded strings.

    Parameters
    ----------
    directory : str
        path of the directory

    strings_to_contain : (str, list)
        strings which the folder and file names need to contain,
        by default ['']

    mode : str, optional
        'any' - only one element of 'strings_to_contain' has to be present
        'all' - all elements of 'strings_to_contain' have to be present,
            by default 'any'

    Returns
    -------
    list
        list of the paths of the folders in the directory which follow the requirements.
    """
    dir_list = list_directory(directory, strings_to_contain, mode)

    return [f for f in dir_list if os.path.isfile(f)]
