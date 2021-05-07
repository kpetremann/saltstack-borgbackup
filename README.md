# Saltstack modules for BorgBackup

## Execution modules

#### latest

```python
latest(repository_path)
```

Get latest archive in repository.

**Arguments**:

- `repository_path`: path of BorgBackup repository

#### archives

```python
archives(repository_path)
```

List BorgBackup archives.

**Arguments**:

- `repository_path`: path of BorgBackup repository

#### info

```python
info(repository_path, archive="")
```

Get repository or archive information.

**Arguments**:

- `repository_path`: path of BorgBackup repository
- `archive`: name of archive

#### explore

```python
explore(repository_path, archive, inpath="")
```

List BorgBackup archive content.

**Arguments**:

- `repository_path`: path of BorgBackup repository
- `archive`: name of archive
- `inpath`: path of directory or file in the archive

#### extract

```python
extract(repository_path, archive, inpath, target, strip_components=0, test=False)
```

Extract file or directory from BorgBackup archive.

**Arguments**:

- `repository_path`: path of BorgBackup repository
- `archive`: name of archive
- `inpath`: path of directory or file in the archive to extract
- `target`: destination of the extract
- `strip_components`: remove the specified number of leading path elements

# State modules

#### restore\_file

```python
restore_file(name, repository_path, archive, target_dir=None)
```

Restore file from BorgBackup archive.

If target_dir is not defined, the backup will be restored in original place.

**Arguments**:

- `name`: path of item in the archive to restore
- `repository_path`: path of BorgBackup repository
- `archive`: name of archive
- `target_dir`: destination of the restoration, default is original path

#### restore\_directory

```python
restore_directory(name, repository_path, archive, target_dir=None, overwrite=False)
```

Restore from BorgBackup archive.

If target_dir is not defined, the backup will be restored in place.

**Arguments**:

- `name`: path of item in the archive to restore
- `repository_path`: path of BorgBackup repository
- `archive`: name of archive
- `target_dir`: destination of the restoration, default is original path
- `overwrite`: overwrite directory in target_dir
