# duplicity-rclone
[Duplicity](http://duplicity.nongnu.org/) backend using [rclone](http://rclone.org/)

Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.

At the time of deveopment, I was using duplicity v0.7.10 and Amazon Cloud Drive, but this backend should work with any storage provider supported by rclone, and with later version of duplicity.\
I am currently running it with duplicity v0.8.12 and rclone v1.51.0, without issues.

Since I've never wrote Python before today, use it at your own risk. Every feedback, comment or suggestion is welcome.

**Update 23/03/2020:** This project has been **merged into official duplicity codebase, since version 0.8.09**, so basically this will remain only for people still running version 0.7.x on older distributions.

**Update 12/05/2020:** After rclone released some new dedicated commands to handle single files, I modified the backend curretnly shipped with duplicity 0.8.x, this code is a lot more efficient in dealing with the storage provider, and fixes a small bug. I hope this code will be merged into the official repository too. I will keep the 0.7.x branch for whoever should still need it.

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
