"""Async task handling helper.

"""
from celery import group

from utils.session import Session
from utils.arrays import flatten

from . import tasks

def fanout(taskname, iterable, block=True, **kwargs):
    """Run a passed function asynchronously."""
    if not isinstance(iterable, (tuple, list)):
        iterable = [iterable]

    def new_task(taskname, *args):
        return getattr(tasks, taskname).s(*args)

    jobs = group(new_task(taskname, item) for item in iterable)
    jobs.set(**kwargs)

    enqueued = jobs.apply_async() # start the jobs
    if block:
        results = enqueued.get()
        return flatten(results)
    return job

def fanout_by_session(taskname, sessions=None, **kwargs):
    """Fanout a task by passed sessions."""
    if not sessions:
        sessions = Session.available_sessions()
    return fanout(taskname, sessions, **kwargs)


def connect_to_bills(sessions=None):
    return fanout_by_session("connect_to_bills", sessions)

def fetch_bills(sessions=None):
    return fanout_by_session("fetch_bills", sessions)

# import gevent
# import requests
#
# import gevent.monkey
# gevent.monkey.patch_socket()
#
# from gevent.pool import Pool
# from utils.arrays import flatten
#
# CONCURRENCY = 3
#
# def run(func, arglist, fanout=True, concurrency=CONCURRENCY, callback=None):
#     """Run a passed function asynchronously."""
#     if not isinstance(arglist, (tuple, list)):
#         arglist = [arglist]
#
#     if fanout: # one job for each arg
#         pool = Pool(size=concurrency)
#         results = pool.map(func, arglist)
#         return flatten(results)
#     # single job with all args
#     return gevent.spawn(func, *arglist).get()

#
# def fetch(url):
#     print('Fetching %s' % url)
#     resp = requests.get(url)
#     data = resp.text
#     print('%s: %s bytes: %r' % (url, len(data), data[:50]))
#     return resp
