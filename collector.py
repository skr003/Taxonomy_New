#!/usr/bin/env python3
import os
import hashlib
import json
import pwd
import grp
from datetime import datetime

OUTPUT_FILE = "/home/jenkins/forensic/output/forensic_data.json"

TARGET_PATHS = [
    "/var/log/", "/var/log/auth.log", "/var/log/secure", "/var/log/syslog",
    "/var/log/messages", "/var/log/dmesg", "/var/log/kern.log", "/var/log/faillog",
    os.path.expanduser("~/.bash_history"), "/var/log/lastlog", "/var/run/utmp",
    "/var/log/wtmp", "/var/log/btmp", "/home/", "/etc/hosts", "/etc/hostname",
    "/etc/resolv.conf", "/etc/ssh/", "/proc/net/", "/etc/passwd", "/etc/shadow",
    "/etc/group", "/etc/sudoers", "/etc/", "/etc/crontab", "/var/spool/cron/",
    "/etc/systemd/", "/usr/lib/systemd/", "/proc/", "/proc/meminfo", "/proc/cpuinfo",
    "/dev/shm/", "/lost+found/", "/media/", "/mnt/", "/var/lib/dpkg/", "/var/lib/rpm/",
    "/etc/apt/sources.list", "/var/log/apt/history.log", "/var/log/yum.log", "/tmp", "/var/tmp"
]

def get_file_hash(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None

def get_metadata(path):
    try:
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "atime": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "ctime": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "owner": pwd.getpwuid(stat.st_uid).pw_name,
            "group": grp.getgrgid(stat.st_gid).gr_name,
            "mode": oct(stat.st_mode),
        }
    except Exception:
        return None

def process_path(path):
    results = []
    if os.path.isfile(path):
        results.append({
            "path": path,
            "hash": get_file_hash(path),
            "metadata": get_metadata(path),
        })
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                full_path = os.path.join(root, f)
                results.append({
                    "path": full_path,
                    "hash": get_file_hash(full_path),
                    "metadata": get_metadata(full_path),
                })
    return results

def main():
    all_results = []
    for path in TARGET_PATHS:
        all_results.extend(process_path(path))
    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_results, f, indent=2)

if __name__ == "__main__":
    main()
