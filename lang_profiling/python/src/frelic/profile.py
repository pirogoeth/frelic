# -*- coding: utf-8 -*-
from __future__ import print_function

import collections
import inspect
import os
import sys
import time

_funcs_prof = {}
_profile = []
_code_cache = {}

BLACKLIST = 0x1
WHITELIST = 0x2

NO_TRACE = set({
    'Cookie',
    'UserDict',
    '_weakrefset',
    'abc',
    'collections',
    'cookielib',
    'decimal',
    'distutils',
    'encodings',
    'eventlet',
    'genericpath',
    'gettext',
    'glob',
    'inspect',
    'locale',
    'logging',
    'netaddr',
    'pkg_resources',
    'positional',
    'posixpath',
    'pytz',
    're',
    'requests',
    'simplejson',
    'six',
    'sre_compile',
    'sre_parse',
    'stat',
    'string',
    'thread',
    'threading',
    'warnings',
    'wrapt',
})

func_prof_res = collections.namedtuple('ProfileRes', 'code_obj function exec_time')

_TRACE_LIMIT = BLACKLIST
_ONLY_TRACE = set({})

def add_trace(modname):
    """ Adds a module to the trace whitelist set.
        Since the user is attempting to add a module name to trace, also enable
        the WHITELIST trace limit.
    """

    global _TRACE_LIMIT
    global _ONLY_TRACE

    if _TRACE_LIMIT is not WHITELIST:
        _TRACE_LIMIT = WHITELIST

    _ONLY_TRACE.add(modname)


def _generic_trace(frame, event, arg):

    # frame -> current stack frame
    # event -> code event type, one of:
    #          call,
    #          line,
    #          return,
    #          exception,
    #          c_call,
    #          c_return,
    #          c_exception
    # arg   -> depends on event type

    try:
        if frame.f_code.co_filename in _code_cache:
            src_module = _code_cache.get(frame.f_code.co_filename)
        else:
            src_module = inspect.getmodule(frame).__name__
            src_module = src_module.split('.')[0]
            _code_cache.update({
                frame.f_code.co_filename: src_module
            })

        if _TRACE_LIMIT is BLACKLIST:
            if src_module in NO_TRACE:
                return
        elif _TRACE_LIMIT is WHITELIST:
            if src_module not in _ONLY_TRACE:
                return
    except:
        # Could not get module :(
        return

    tb = inspect.getframeinfo(frame)

    if event == 'call':
        _funcs_prof.update({
            tb.function: time.time()
        })

        return _generic_trace
    elif event == 'return':
        if tb.function in _funcs_prof:
            _exec_time = time.time() - _funcs_prof.pop(tb.function)
            _profile.append(
                func_prof_res(
                    code_obj=frame.f_code,
                    function=tb.function,
                    exec_time=_exec_time))
        else:
            _exec_time = -1

    return


def build_profiling_info():

    _funcs = {}
    for tup in _profile:
        uniq = '%s#%s' % (tup.code_obj.co_filename, tup.function)
        if uniq not in _funcs:
            _funcs.update({
                uniq: {
                    'function': tup.function,
                    'filename': tup.code_obj.co_filename,
                    'lineno': tup.code_obj.co_firstlineno,
                    'times': [],
                },
            })

        _funcs.get(uniq).get('times').append(tup.exec_time)

    for uniq, data in _funcs.items():
        stats = {
            'total': sum(data.get('times')),
            'max': max(data.get('times')),
            'min': min(data.get('times')),
            'avg': sum(data.get('times')) / len(data.get('times')),
        }
        data.update({
            'stats': stats
        })

    return _funcs


def print_profiling_info():

    _totals = {}

    profiled_info = build_profiling_info()
    for uniq, data in profiled_info.items():
        function = data.get('function')
        filename = data.get('filename')
        times = data.get('times')

        print(' ---> profiled function : %s # %s' % (filename, function))
        total_exec = sum(times)

        runnum = 1
        for et in times:
            print('     -> #%s : %s' % (runnum, et))
            runnum += 1
        print(' ===> spent %s seconds in function\n' % (total_exec))
        _totals.update({
            function: total_exec
        })

    prog_exec = sum(_totals.values())
    _key_func = lambda p: p[1]
    longest_func = max(zip(_totals.keys(), _totals.values()), key=_key_func)

    print(' ---> largest function %s ran for %s%% of runtime (%s secs)' % (
        longest_func[0],
        (longest_func[1] / prog_exec) * 100,
        longest_func[1]))


    return _totals


def install_profiler(install_atexit=False):

    if install_atexit:
        import atexit
        atexit.register(print_profiling_info)

    sys.settrace(_generic_trace)


def remove_profiler(remove_atexit=False):

    if remove_atexit:
        import atexit
        # This is a hack but okay :(
        if print_profiling_info in atexit._exithandlers:
            atexit._exithandlers.remove(print_profiling_info)

    sys.settrace(None)
