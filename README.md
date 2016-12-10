# duplicity-rclone
Duplicity backend using [rclone](http://rclone.org/)

Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

This backend has been developed for duplicity 0.7.10, and tested with Amazon Cloud Drive only. Since I've never wrote Python before today, use it at your own risk. Every feedback, comment or suggestion is welcome.

# Setup
Install `rclonebackend.py` into duplicity backend directory. This backend provides support for prefix `rclone://`.

# Usage
Once you have configured rclone and successfully set up a remote (e.g. `acd` for Amazon Cloud Drive), you can start your backup with
```
duplicity /mydocuments rclone://acd:/mydocuments
```
