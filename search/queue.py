"""Async task handling helper.

"""
from celery import group
from celery.app.control import Inspect
from service import celery_app

from utils.session import Session
from utils.arrays import flatten

from . import tasks

def is_available():
    """Boolean for whether celery has nodes available for async tasks."""
    return True if Inspect(app=celery_app).ping() else False

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
        return results
    return job

def fanout_by_session(taskname, sessions=None, **kwargs):
    """Fanout a task by passed sessions."""
    if not sessions:
        sessions = Session.available_sessions()
    return fanout(taskname, sessions, **kwargs)


def connect_to_bills(sessions=None):
    connected = fanout_by_session("connect_to_bills", sessions)
    return (
        flatten(actids for actids, billids in connected),
        flatten(billids for actids, billids in connected),
    )

def fetch_bills(sessions=None):
    return fanout_by_session("fetch_bills", sessions)
