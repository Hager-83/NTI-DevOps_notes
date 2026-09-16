# Session 5 — Linux Commands

**Date:** 24 Aug 2026

## 1. Archive & Compression — `tar`

`tar` is used to create archives, compress them, and extract them.

### Create an archive
```bash
tar -cvf file.name /dir_name
```
- `-c` create
- `-v` verbose
- `-f` filename
- **Use:** make an archive/backup of a directory.

### Create a compressed archive
```bash
tar -czf new_file_name file.name
```
- `-c` create
- `-z` gzip compression
- `-f` filename
- **Use:** create a compressed `.tar.gz` archive.

### Check size
```bash
du -sh new_file_name
```
- `-s` total size
- `-h` human-readable
- **Use:** check the archive size.

### Extract
```bash
tar -xzf file.name
```
- `-x` extract
- `-z` gzip
- `-f` filename
- **Use:** extract a `.tar.gz` archive.

---

## 2. File Transfer — `scp`

`scp` (Secure Copy) copies files between local and remote machines.

### Send a file
```bash
scp file_to_send user@IP:location
```
**Use:** local → remote.

### Get a file
```bash
scp user@IP:/location/file_name .
```
`.` means the current local directory.

**Use:** remote → local.

### Send a directory
```bash
scp -r dir_to_send user@IP:location
```

### Get a directory
```bash
scp -r user@IP:/location/dir_name .
```

`-r` is used for directories because their contents are copied recursively.

---

## 3. Remote File Access — `sftp`

### Connect
```bash
sftp user@IP
```
**Use:** start an interactive file-transfer session.

### Local vs Remote

| Command | Meaning |
|---|---|
| `lpwd` | Show local working directory |
| `pwd` | Show remote working directory |
| `lls` | List local files |
| `ls` | List remote files |

### Transfer files

```bash
put file_name
```
**Use:** local → remote.

```bash
get file_name
```
**Use:** remote → local.

```bash
exit
```
**Use:** leave the SFTP session.

---

## 4. System & Package Information

### Ubuntu release information
```bash
cat /etc/ubuntu-release
```
**Use:** check OS release information as written in the session notes.

### System information
```bash
uname -a
```
**Use:** show kernel/system information.

---

## 5. RPM Package Management

An RPM package has fields such as:

```text
Name | Version | Release | Architecture
```

### List all installed packages
```bash
rpm -qa
```
- `-q` query
- `-a` all
- **Use:** list installed RPM packages.

### Query a package
```bash
rpm -q pkg_name
```
**Use:** check/query a package.

### Find a package in the installed list
```bash
rpm -qa | grep pkg_name
```
**Use:** search installed packages by name.

### List all files installed by a package
```bash
rpm -ql pkg_name
```
**Use:** see where the package installed files.

### Show configuration files
```bash
rpm -qc pkg_name
```
**Use:** find the package's configuration files.

### Show documentation/man pages
```bash
rpm -qd pkg_name
```
**Use:** find documentation files.

### Remove a package
```bash
rpm -ev pkg_name
```
- `-e` erase/remove
- `-v` verbose
- **Use:** uninstall an RPM package.

---

## 6. RPM vs YUM vs DNF

### RPM
Works directly with RPM packages.

**Important:** RPM does not automatically resolve/install dependencies.

### YUM
Repository-based package manager.

The session comparison:
```text
YUM on RHEL/CentOS ≈ APT on Ubuntu
```

### DNF
Newer package-management tool related to the YUM workflow.

**Key idea:**
```text
RPM → direct package operations
YUM → repository-based management
DNF → newer repository/package manager with dependency handling
```

---

## 7. Repositories, AppStream & BaseOS

The session covered:
- **Repositories:** sources where packages are provided.
- **AppStream:** application packages/metadata.
- **BaseOS:** core operating-system packages.

The ISO may need to be mounted so the system can access AppStream and BaseOS.

---

## 8. Mounting

### Check disk usage
```bash
df -h
```
- `-h` human-readable
- **Use:** check filesystem/disk space.

### Mount ISO/device
```bash
mount -o loop /dev/sr0 /media
```
- `-o loop` mounts the image/device through a loop interface.
- `/dev/sr0` is the optical-media device used in the notes.
- `/media` is the mount point.
- **Use:** make ISO/optical-media contents accessible through a directory.

---

# Recommended Session Workflow

```bash
tar -czf backup.tar.gz /dir_name
du -sh backup.tar.gz
scp backup.tar.gz user@IP:/location

sftp user@IP
put file_name
get file_name

rpm -qa
rpm -q pkg_name
rpm -ql pkg_name
rpm -qc pkg_name
rpm -qd pkg_name

df -h
mount -o loop /dev/sr0 /media
```

# Quick Revision

| Command | Purpose | Use when |
|---|---|---|
| `tar -cvf` | Create archive | Make a backup/archive |
| `tar -czf` | Compress/archive | Create `.tar.gz` |
| `du -sh` | Show size | Check archive size |
| `tar -xzf` | Extract | Restore archive |
| `scp` | Copy files | Quick local/remote transfer |
| `scp -r` | Copy directories | Transfer a directory |
| `sftp` | Remote transfer session | Interactive transfer |
| `put` | Upload | Local → remote |
| `get` | Download | Remote → local |
| `lpwd` / `lls` | Local info | SFTP local side |
| `pwd` / `ls` | Remote info | SFTP remote side |
| `rpm -qa` | List packages | See installed RPMs |
| `rpm -q` | Query package | Check a package |
| `rpm -ql` | Package files | Find installed files |
| `rpm -qc` | Config files | Find configuration |
| `rpm -qd` | Documentation | Find docs/man pages |
| `rpm -ev` | Remove package | Uninstall |
| `uname -a` | System info | Check kernel/system |
| `df -h` | Disk usage | Check storage |
| `mount -o loop` | Mount image | Access ISO contents |

## Important Notes

- `scp` is simple for individual copy operations; `sftp` gives you an interactive transfer session.
- In SFTP: **`put` = send**, **`get` = receive**.
- In SFTP: **`l` means local**, so `lpwd` and `lls` refer to the local machine.
- `rpm` handles RPM packages directly; the session notes emphasize that it does not automatically handle dependencies.
- YUM/DNF work with repositories and dependency handling.
- Mounting the ISO is needed in the session to access **AppStream** and **BaseOS** content.
