"""Invoke tasks."""
import os

from invoke import task  # type: ignore

PATH = os.path.dirname(os.path.realpath(__file__))


@task
def install(cmd):
    """Install virtualenv."""
    cmd.run(f"python -m venv {PATH}/.venv")
    with cmd.prefix(f"source {PATH}/.venv/bin/activate"):
        cmd.run(f"pip install -r {PATH}/test-requirements.txt")


@task
def reformat(cmd):
    """Auto format using black and isort."""
    with cmd.prefix(f"source {PATH}/.venv/bin/activate"):
        cmd.run(f"isort {PATH}/_modules {PATH}/_states")
        cmd.run(f"black {PATH}/_modules {PATH}/_states")
