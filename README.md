# duplicity-rclone
[Duplicity](http://duplicity.nongnu.org/) backend using [rclone](http://rclone.org/)

Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

At the time of deveopment, I was using duplicity v0.7.10 and Amazon Cloud Drive, but this backend should work with any storage provider supported by rclone, and with later version of duplicity.\
I am currently running it with duplicity v0.7.17 and rclone v1.43.1, without issues.

Since I've never wrote Python before today, use it at your own risk. Every feedback, comment or suggestion is welcome.

**Update 19/05/2017:** Since Amazon banned rclone, I moved my data to Google Drive, and it works smoothly as expected.

**Update 23/03/2020:** This project has been **merged into official duplicity codebase, since version 0.8.09**, so basically this will remain only for people still running version 0.7.x on older distributions.

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
**Please note the slash after the second colon.** Some storage provider will work with or without slash after colon, but some other will not. Since duplicity will complain about malformed URL if a slash is not present, **always put it after the colon**, and the backend will handle it for you.
