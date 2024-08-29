from threading import Thread
import concurrent.futures
from multiprocessing import Pool, Process
from functools import partial

__all__ = [
    'run_in_thread',
    'threaded',
    'run_in_process',
    'parallel',
]

def run_in_thread(function, daemon=True):
    """
    Run function in another thread.
    Caller with no longer be blocked by this function, but also will not
    be able to catch exception or get results from function.
    Parameters
    ----------
    function : function
        The function which shall be wrapper

    daemon: bool
        Set the thread to be daemon, by default True.

    Returns
    -------
    function
        The wrapper function

    Example
    -------
    ```python
    @run_in_thread(daemon=True)
    def task1():
        do_something

    @run_in_thread(daemon=True)
    def task2():
        do_something_else
    ...
    t1 = task1()
    t2 = task2()
    ...
    t1.join()
    t2.join()
    ```
    """
    if function is None:
        """A partial is a "non-complete function call" that includes
        a function and some arguments, so that they are passed around
        as one object without actually calling the function yet.
        """
        return partial(run_in_thread, daemon=daemon)

    @wraps(function)  # maintain all the info about the function
    def wrapper(*func_args, **func_kwargs):
        thread = Thread(target=function,
                        args=func_args, kwargs=func_kwargs,
                        daemon=daemon)
        thread.start()
        return thread
    return wrapper

def threaded(function):
    @wraps(function)  # maintain all the info about the function
    def wrapper(*func_args, **func_kwargs):
        results = {}
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = {executor.submit(function, [i]): idx for idx,
                       i in enumerate(func_args[0])}

            tasks = len(futures)
            tenth = round(tasks / 10)
            print('Formed pool of {} tasks'.format(tasks))

            for idx, future in enumerate(concurrent.futures.as_completed(futures)):
                i = futures[future]
                try:
                    # store result
                    data = future.result()
                    # check to see if in array form
                    if len(data) == 1:
                        data = data[0]
                    results[i] = data
                except Exception as exc:
                    print('{} generated an exception: {}'.format(
                        func_args[0][i], exc))

                if tenth != 0 and idx != 0 and idx % tenth == 0:
                    print('{}% Done'.format((idx // tenth) * 10))

        # sort and put in array
        final = []
        for k, v in sorted(results.items()):
            final.append(v)

        return final
    return wrapper

def run_in_process(function):
    """
    Run function in another thread.
    Caller with no longer be blocked by this function, but also will not
    be able to catch exception or get results from function.
    Parameters
    ----------
    function : function
        The function which shall be wrapper

    daemon: bool
        Set the thread to be daemon, by default True.

    Returns
    -------
    function
        The wrapper function

    Example
    -------
    ```python
    @run_in_thread(daemon=True)
    def task1():
        do_something

    @run_in_thread(daemon=True)
    def task2():
        do_something_else
    ...
    t1 = task1()
    t2 = task2()
    ...
    t1.join()
    t2.join()
    ```
    """

    @wraps(function)  # maintain all the info about the function
    def wrapper(*func_args, **func_kwargs):
        process = Process(target=function,
                        args=func_args, kwargs=func_kwargs)
        process.start()
        return process
    return wrapper

def parallel(function, nb_processes=None):
    """
    Works similar to a decorator to parallelize "stupidly parallel"
    problems. Decorators and multiprocessing don't play nicely because
    of naming issues.

    Parameters
    ----------
    function : function:
        the function that will be parallelized. The FIRST
        argument is the one to be iterated on (in parallel). The other
        arguments are the same in all the parallel runs of the function
        (they can be named or unnamed arguments).

    nb_processes : int:
        the number of processes to run.
        It is passed to multiprocessing.Pool, by default None

    Returns
    -------
    function:
        the wrapper function


    Example
    -------
    >>> def square_and_offset(value, offset=0):
    ...     return value**2 + offset
    ... parallel_square_and_offset = parallel(square_and_offset,
                                       nb_processes=5)
    >>> print(parallel_square_and_offset(range(10), offset=3))
    [3, 4, 7, 12, 19, 28, 39, 52, 67, 84]

    """
    @wraps(function)  # maintain all the info about the function
    def wrapper(iterable_values, *args, **kwargs):
        args = list(args)
        pool = Pool(nb_processes)
        result = [pool.apply_async(function, args=[value]+args,
                                kwds=kwargs)
                  for value in iterable_values]
        pool.close()
        return [r.get() for r in result]
    return wrapper