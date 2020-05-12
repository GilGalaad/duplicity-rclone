"""
Duplicity backend using rclone
Rclone is a powerful command line program to sync files and directories to and from various cloud storage providers.
File name: rclonebackend.py
Author: Francesco Magno
Date created: 12/05/2020
Licence: GPL-2.0
Repository: https://github.com/GilGalaad/duplicity-rclone
Python Version: 3.7
"""

from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object

import os
import os.path
import sys

import duplicity.backend
from duplicity import path
from duplicity import log
from duplicity.errors import BackendException
from duplicity import util


class RcloneBackend(duplicity.backend.Backend):

    def __init__(self, parsed_url):
        duplicity.backend.Backend.__init__(self, parsed_url)
        self.rclone_cmd = u"rclone"
        self.parsed_url = parsed_url
        self.remote_path = self.parsed_url.path

        try:
            rc, o, e = self.subprocess_popen(
                self.rclone_cmd + u" --version")
        except Exception:
            log.FatalError(u"rclone not found: please install rclone", log.ErrorCode.backend_error)

        if parsed_url.path.startswith(u"//"):
            self.remote_path = self.remote_path[2:].replace(u":/", u":", 1)

        self.remote_path = util.fsdecode(self.remote_path)

    def _get(self, remote_filename, local_path):
        remote_filename = util.fsdecode(remote_filename)
        local_pathname = util.fsdecode(local_path.name)
        commandline = u"%s copyto %s/%s %s" % (
            self.rclone_cmd, self.remote_path, remote_filename, local_pathname)
        rc, o, e = self.subprocess_popen(commandline)
        if rc != 0:
            if os.path.isfile(local_pathname):
                os.remove(local_pathname)
            raise BackendException(e.split(u'\n')[0])

    def _put(self, source_path, remote_filename):
        source_pathname = util.fsdecode(source_path.name)
        remote_filename = util.fsdecode(remote_filename)
        commandline = u"%s copyto %s %s/%s" % (
            self.rclone_cmd, source_pathname, self.remote_path, remote_filename)
        rc, o, e = self.subprocess_popen(commandline)
        if rc != 0:
            raise BackendException(e.split(u'\n')[0])

    def _list(self):
        filelist = []
        commandline = u"%s lsf %s" % (
            self.rclone_cmd, self.remote_path)
        rc, o, e = self._subprocess_safe_popen(commandline)
        if rc == 3:
            return filelist
        if rc != 0:
            raise BackendException(e.split(u'\n')[0])
        if not o:
            return filelist
        return [util.fsencode(x) for x in o.split(u'\n') if x]

    def _delete(self, remote_filename):
        remote_filename = util.fsdecode(remote_filename)
        commandline = u"%s deletefile --drive-use-trash=false %s/%s" % (
            self.rclone_cmd, self.remote_path, remote_filename)
        rc, o, e = self.subprocess_popen(commandline)
        if rc != 0:
            raise BackendException(e.split(u'\n')[0])

    def _subprocess_safe_popen(self, commandline):
        import shlex
        from subprocess import Popen, PIPE
        args = shlex.split(commandline)
        p = Popen(args, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        stdout, stderr = p.communicate()
        return p.returncode, stdout, stderr


duplicity.backend.register_backend(u"rclone", RcloneBackend)
