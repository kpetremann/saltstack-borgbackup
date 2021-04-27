"""
State module for BorgBackup (https://borgbackup.readthedocs.io/en/stable/).

:codeauthor: Kevin Petremann <kpetrem@gmail.com>
:maturity:   new
:depends:    borgbackup
:platform:   all (tested only on linux)
"""
from pathlib import Path

__virtual_aliases__ = ("borg",)


def __virtual__():
    if not __utils__["path.which"]("borg"):
        return (False, "The borg execution module cannot be loaded: borg unavailable.")
    return True


def _get_level_strip_components(name):
    # get the level of the item in the backup tree
    path_parts = Path(name).parts
    nb_level = len(path_parts) - 2

    if nb_level < 0:
        nb_level = 0

    return nb_level


def restore_file(name, repository_path, archive, target_dir=None):
    """
    Restore file from BorgBackup archive.

    If target_dir is not defined, the backup will be restored in original place.

    :param name: path of item in the archive to restore
    :param repository_path: path of BorgBackup repository
    :param archive: name of archive
    :param target_dir: destination of the restoration, default is original path
    """
    ret = {
        "changes": {},
        "comment": "",
        "name": "later",
        "result": False,
    }

    if not target_dir:
        target_dir = str(Path(name).parent)

    # get the level of the item in the backup tree
    nb_level = _get_level_strip_components(name)

    # restore the item
    __salt__["borg.extract"](
        repository_path=repository_path,
        archive=archive,
        inpath=name,
        target=target_dir,
        strip_components=nb_level,
    )

    return ret


def restore_directory(name, repository_path, archive, target_dir=None, overwrite=False):
    """
    Restore from BorgBackup archive.

    If target_dir is not defined, the backup will be restored in place.

    :param name: path of item in the archive to restore
    :param repository_path: path of BorgBackup repository
    :param archive: name of archive
    :param target_dir: destination of the restoration, default is original path
    :param overwrite: overwrite directory in target_dir
    """
    ret = {
        "name": name,
        "changes": {},
        "comment": "",
        "result": None,
    }
    item_path = Path(name)
    directory_name = item_path.name

    # it target directory not defined, we restore in the original path
    if not target_dir:
        target_dir = str(item_path.parent)

    # removing existing directory if requested
    if overwrite:
        to_clean = str(Path(target_dir).joinpath(directory_name))
        res = __states__["file.absent"](to_clean)
        ret["changes"]["clean"] = res.get("changes")
        ret["comment"] += res.get("comment")
        ret["result"] = res.get("result")

    # get the level of the item in the backup tree
    nb_level = _get_level_strip_components(name)

    # restore the item
    res = __salt__["borg.extract"](
        repository_path=repository_path,
        archive=archive,
        inpath=name,
        target=target_dir,
        strip_components=nb_level,
        test=__opts__["test"],
    )

    ret["changes"]["restored"] = res.get("changes")
    ret["comment"] += "\n" + res.get("comment")
    ret["result"] = ret["result"] and res.get("result")

    return ret
