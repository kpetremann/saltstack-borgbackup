"""
Execution module for BorgBackup (https://borgbackup.readthedocs.io/en/stable/).

:codeauthor: Kevin Petremann <kpetrem@gmail.com>
:maturity:   new
:depends:    borgbackup
:platform:   all (tested only on linux)
"""
import os
import json

__virtual_aliases__ = ("borg",)


def __virtual__():
    if not __utils__["path.which"]("borg"):
        return (False, "The borg execution module cannot be loaded: borg unavailable.")
    return True


def latest(repository_path):
    """
    Get latest archive in repository.

    :param repository_path: path of BorgBackup repository
    """
    result = __salt__["cmd.run"](f"borg list --json {repository_path} --last 1")
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return result


def archives(repository_path):
    """
    List BorgBackup archives.

    :param repository_path: path of BorgBackup repository
    """
    result = __salt__["cmd.run"](f"borg list --json {repository_path}")
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return result


def info(repository_path, archive=""):
    """
    Get repository or archive information.

    :param repository_path: path of BorgBackup repository
    :param archive: name of archive
    """
    path = f"{repository_path}::{archive}" if archive else repository_path

    result = __salt__["cmd.run"](f"borg info --json {path}")
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return result


def explore(repository_path, archive, inpath=""):
    """
    List BorgBackup archive content.

    :param repository_path: path of BorgBackup repository
    :param archive: name of archive
    :param inpath: path of directory or file in the archive
    """
    result = __salt__["cmd.run"](f"borg list --json-lines {repository_path}::{archive} {inpath}")

    decoded = []
    try:
        for line in result.splitlines():
            decoded.append(json.loads(line))
    except json.JSONDecodeError:
        return result

    return decoded


def extract(repository_path, archive, inpath, target, strip_components=0, test=False):
    """
    Extract file or directory from BorgBackup archive.

    :param repository_path: path of BorgBackup repository
    :param archive: name of archive
    :param inpath: path of directory or file in the archive to extract
    :param target: destination of the extract
    :param strip_components: remove the specified number of leading path elements
    """
    result = None

    in_archive_path = inpath.lstrip(os.sep)
    dry_run = "-n" if test else ""

    cmd = (
        f"borg extract --strip-components {strip_components} "
        f"{dry_run} {repository_path}::{archive} {in_archive_path}"
    )

    res = __salt__["cmd.run"](cmd, cwd=target)
    result = __context__["retcode"] == 0

    changes = f"{repository_path}::{archive} {inpath} restored to {target}" if result else ""

    if test and result:
        changes = f"dry-run: {repository_path}::{archive} {inpath} restored to {target}"
        result = None

    return {
        "changes": changes,
        "comment": res,
        "result": result,
    }
