# duplicity-rclone
Duplicity backend using [rclone](http://rclone.org/)

Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

At the time of deveopment, I was using duplicity 0.7.10 and Amazon Cloud Drive, but this backend should work with any storage provider supported by rclone, and with later version of duplicity. 

Since I've never wrote Python before today, use it at your own risk. Every feedback, comment or suggestion is welcome.

**Update 19/05/2017:** Since Amazon banned rclone, I moved my data to Google Drive, and it works smoothly as expected.

# Setup
Install `rclonebackend.py` into duplicity backend directory. This backend provides support for prefix `rclone://`.

# Usage
Once you have configured rclone and successfully set up a remote (e.g. `gdrive` for Google Drive), assuming you can list your remote files with
```
rclone ls gdrive:mydocuments
```
you can start your backup with
```
duplicity /mydocuments rclone://gdrive:/mydocuments
```
**Please note the slash after colon.** Some storage provider will work with or without slash after colon, but some other will not work because assume the first word is the bucket/container. But since dupicity will complain about malformed URL if a slash is not present, always put it after the colon, and the backend will remove it in the process.
