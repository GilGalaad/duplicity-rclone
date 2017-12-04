import os
import os.path

import duplicity.backend
from duplicity import path
from duplicity import log
from duplicity.errors import BackendException

class RcloneBackend(duplicity.backend.Backend):

	def __init__(self, parsed_url):
		duplicity.backend.Backend.__init__(self, parsed_url)
		self.rclone_cmd = "rclone"
		self.parsed_url = parsed_url
		self.remote_path = self.parsed_url.path

		try:
			rc, o, e = self._subprocess(self.rclone_cmd + " version")
		except Exception:
			log.FatalError("rclone not found: please install rclone", log.ErrorCode.backend_error)

		if parsed_url.path.startswith("//"):
			self.remote_path = self.remote_path[2:].replace(":/",":",1)

	def _get(self, remote_filename, local_path):
		temp_dir = os.path.dirname(local_path.name)
		commandline = "%s copy %s/%s %s" % (self.rclone_cmd, self.remote_path, remote_filename, temp_dir)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			if os.path.isfile(os.path.join(temp_dir, remote_filename)):
				os.remove(os.path.join(temp_dir, remote_filename))
			raise BackendException(e.split('\n')[0])
		os.rename(os.path.join(temp_dir, remote_filename), local_path.name)

	def _put(self, source_path, remote_filename):
		temp_dir = os.path.dirname(source_path.name)
		temp_filename = os.path.basename(source_path.name)
		os.rename(source_path.name, os.path.join(temp_dir, remote_filename))
		commandline = "%s copy --include %s %s %s" % (self.rclone_cmd, remote_filename, temp_dir, self.remote_path)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			os.rename(os.path.join(temp_dir, remote_filename), source_path.name)
			raise BackendException(e.split('\n')[0])
		os.rename(os.path.join(temp_dir, remote_filename), source_path.name)

	def _list(self):
		filelist = []
		commandline = "%s ls %s" % (self.rclone_cmd, self.remote_path)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			if e.endswith("not found\n"):
				return filelist
			else:
				raise BackendException(e.split('\n')[0])
		if not o:
			return filelist
		lines = o.split('\n')
		for x in lines:
			if x:
				filelist.append(x.split()[-1])
		return filelist

	def _delete(self, remote_filename):
		commandline = "%s delete --include %s %s" % (self.rclone_cmd, remote_filename, self.remote_path)
		rc, o, e = self._subprocess(commandline)
		if rc != 0:
			raise BackendException(e.split('\n')[0])

	def _subprocess(self, commandline):
		import shlex
		from subprocess import Popen, PIPE
		args = shlex.split(commandline)
                private = self.munge_password(commandline)
                log.Info(_("Reading results of '%s'") % private)
		p = Popen(args, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
		return p.returncode, stdout, stderr

duplicity.backend.register_backend("rclone", RcloneBackend)