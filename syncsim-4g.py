#! /usr/bin/env python
#
#

import re
import os
import sys
import shutil
import subprocess
import argparse
__author__ = 'ashlaban'

if __name__ != "__main__":
	raise "Not running as a stand-alone!"

class bcolors:
#	"""
#	Global access for ansi codes.
#
#	Thanks joeld (http://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python).
#	"""
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	@staticmethod
	def print_header( text ):
		print bcolors.HEADER,
		print "=== " + text + " ===",
		print bcolors.ENDC

	@staticmethod
	def print_ok( text ):
		print bcolors.OKBLUE + text + bcolors.ENDC

	@staticmethod
	def print_warning( text ):
		print bcolors.WARNING + text + bcolors.ENDC

	@staticmethod
	def print_fail( text ):
		print bcolors.FAIL + text + bcolors.ENDC

	@staticmethod
	def print_error( msg ):
		print bcolors.FAIL + "Error: " + bcolors.ENDC + msg

	@staticmethod
	def print_ok_msg( prompt, msg ):
		print bcolors.OKBLUE + prompt + " " + bcolors.ENDC + msg

#
# Operates on files. Searching for them, filename management, getting paths etc.
#
class FileHandler(object):
	ALLOWED_FLIE_EXTENSIONS = [".zip", ".tar.bz2", ".tar.gz", ".tar", ".7z", ".rar"]
	ALLOWED_FLIE_EXTENSIONS.sort()
	ALLOWED_FLIE_EXTENSIONS.reverse()

	@staticmethod
	def split_filename(source_path):
		for allowed_ext in FileHandler.ALLOWED_FLIE_EXTENSIONS:
			p = source_path.split(allowed_ext)
			if len(p) == 2:
				basename = p[0]
				ext      = allowed_ext
				return (basename, ext)

		basename = source_path
		ext      = ""
		return (basename, ext)

	@staticmethod
	def get_extension(source_path):
		return FileHandler.split_filename(source_path)[1]

	@staticmethod
	def find_group_file( search_path ):
		group_regex = re.compile('\S*(?:group|grupp)\-?\D?([0-9]+)\S*', re.IGNORECASE)
		lab_regex   = re.compile('\S*lab\-?([0-9]*)([a-c])?\S*'       , re.IGNORECASE)

		for (dirpath, dirnames, filenames) in os.walk(search_path):
			for filename in filenames:
				(basename, ext) = FileHandler.split_filename(filename)
				# print basename, ext
				if (ext == ""):
					continue

				(group_num, )         = group_regex.match( basename ).groups()
				(lab_num, lab_letter) =   lab_regex.match( basename ).groups()

				# Debug print!
				# print basename
				# print group_num
				# print lab_num
				# print args.group
				# print args.lab_name

				if (group_num is None or group_num == ''): continue
				if (lab_num   is None or lab_num   == ''): continue

				# Normalise group and lab numbers
				group_num = int(group_num)
				lab_name  = str(int(lab_num))
				if (not (lab_letter is None) ): lab_name += lab_letter

				if (group_num == args.group and "lab"+lab_name == args.lab_name):
					# print dirpath, filename
					# print basename, ext
					return (dirpath, basename, ext)
		return (None, None, None)

	@staticmethod
	def find_relative_path( root_folder, filename ):
		for (dirpath, dirnames, filenames) in os.walk(root_folder):
			for filename in filenames:
				if filename == filename:
					return dirpath

	@staticmethod
	def create_dir( base_path, path ):
		try:
			os.mkdir( base_path )
		except OSError as exp:
			pass
		try:
			os.mkdir( path )
		except OSError as exp:
			shutil.rmtree( path )
			os.mkdir( path )

	@staticmethod
	def create_initial_file_structure(base_path):
		print 'Creating default file structure.'

		print 'Creating {}/in...'.format(base_path)
		print '\tPut archives here.'
		os.mkdir(base_path+'/in')

		print 'Creating {}/out...'.format(base_path)
		print '\tThis is where archives are unpacked to.'
		os.mkdir(base_path+'/out')


#
# Unpacks files with delegates for different file extensions.
#
# TODO: Update help text to reflect the fact that the program depends on certain installed unpackers.
#
class Unpacker(object):

	@staticmethod
	def unpack( source_path, target_path ):

		extension = FileHandler.get_extension(source_path)

		if extension:
			print "Source archive  : " + archive_name
			print "Target directory: " + out_dir
		else:
			return -1

		if extension == '.tar.gz':
			return Unpacker._unpack_tar(source_path, target_path)
		elif extension == '.tar.bz2':
			return Unpacker._unpack_tar(source_path, target_path)
		elif extension == '.tar':
			return Unpacker._unpack_tar(source_path, target_path)
		elif extension == '.zip':
			return Unpacker._unpack_zip(source_path, target_path)
		elif extension == '.rar':
			return Unpacker._unpack_rar(source_path, target_path)
		elif extension == '.7z':
			return Unpacker._unpack_7z(source_path, target_path)
		else:
			print "Unknown extension: " + extension
			return -1

	@staticmethod
	def _unpack_tar(source_path, target_path):
		# TODO: Hide stdout (redirect to /dev/null), show only stderr.
		program_path = "tar"
		program_opts = ["-xf", source_path, "--directory", target_path]
		program_cmd  = [program_path] + program_opts
		print "Invoking " + program_path + " with args " + " ".join(program_opts)
		return subprocess.call( program_cmd )
	@staticmethod
	def _unpack_zip(source_path, target_path):
		# TODO: Hide stdout (redirect to /dev/null), show only stderr.
		program_path = "unzip"
		program_opts = ["-o", source_path, "-d", target_path]
		program_cmd  = [program_path] + program_opts
		print "Invoking " + program_path + " with args " + " ".join(program_opts)
		return subprocess.call( program_cmd )
	@staticmethod
	def _unpack_rar(source_path, target_path):
		# TODO: Hide stdout (redirect to /dev/null), show only stderr.
		program_path = "unrar"
		program_opts = ["x", source_path, target_path]
		program_cmd  = [program_path] + program_opts
		print "Invoking " + program_path + " with args " + " ".join(program_opts)
		return subprocess.call( program_cmd )
	@staticmethod
	def _unpack_7z(source_path, target_path):
		# TODO: Hide stdout (redirect to /dev/null), show only stderr.
		program_path = "7za"
		program_opts = ["x", "-y", "-o"+target_path, source_path]
		program_cmd  = [program_path] + program_opts
		print "Invoking " + program_path + " with args " + " ".join(program_opts)
		return subprocess.call( program_cmd )

# Define the command line interface
parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	description='''\
Helper script for correcting labs in the LTU course D0013E.
Example use:
	syncsim-4g check -l lab1a -g 1 --output-mem

This will look for a file on the format groupXXX-labYYY.ZZZ, where XXX is a
group number, YYY is the lab designation and ZZZ is a file extention suitable
for a compressed folder. (The file name parser is quite nice with allowed file
names. See exact regex if interested.)

The file will be unpacked, the obj_dump will be sent to SyncSim and the
modified memory locations will be printed on screen.

More configuration options are possible, run
	syncsim-4g check --help
for full specification.
''')

subparsers  = parser.add_subparsers(dest='command')
parser_init = subparsers.add_parser('init', help='Create initial directory structure if it does not exist already.')

parser_check = subparsers.add_parser('check', help='Check a student solution.')
parser_check.add_argument('-l', dest='lab_name', type=str, help='lab name', required=True, choices=['lab1a', 'lab1b', 'lab2', 'lab3a', 'lab3b', 'lab4'])
parser_check.add_argument('-s', dest='syncsim_path', type=str, help='path to syncsim, default=SyncSim.jar', default="SyncSim.jar")
parser_check.add_argument('-g', dest='group' , type=int, help='group number', required=True)
model_group    = parser_check.add_argument_group("MIPS model options", "Mutually exclusive, defaults to non-pipelined model if none of the below are given.")
model_group_ex = model_group.add_mutually_exclusive_group()
model_group_ex.add_argument('-e','--ext' , action='store_true', help='use extended  mips model')
model_group_ex.add_argument('-p','--pipe', action='store_true', help='use pipelined mips model')
output_group = parser_check.add_argument_group("Output options")
output_group.add_argument('-m','--output-mem', action='store_true', help='output memory from syncsim after simulation')
output_group.add_argument('-r','--output-reg', action='store_true', help='output registers from syncsim after simulation')
output_group.add_argument('-o','--output-ow' , action='store_true', help='send output to console instead of output window')
parser_check.add_argument('-c', dest='count', type=int, default=50000, help='number of cycles to run simulation')
parser_check.add_argument('--use-preset', action='store_true', help='applies a default configuration based on lab lame (-l)')
args = parser.parse_args()

if args.command == 'init':
	FileHandler.create_initial_file_structure('.')
	sys.exit(0)

# Set up auxiliary defaults
if (args.use_preset):
	if   (args.lab_name == 'lab1a'): parser.set_defaults(output_mem=True, count=50000)
	elif (args.lab_name == 'lab1b'): parser.set_defaults(output_mem=True, count=150000)
	elif (args.lab_name == 'lab2') : parser.set_defaults(ext=True, output_mem=True, count=150000)
	elif (args.lab_name == 'lab3a'): parser.set_defaults(ext=True, output_ow=True, count=2000)
	elif (args.lab_name == 'lab3b'): parser.set_defaults(ext=True, output_ow=True, count=10000)
	elif (args.lab_name == 'lab4'): pass
# Reparse
args = parser.parse_args()

# Print configuration information
bcolors.print_header( "Configuration" )
print "Group name: " +"group"+ str(args.group)
print "Lab name  : " + args.lab_name
if (args.pipe)      : print "Using pipelined model."
if (args.output_mem): print "Printing touched memory after simulation."
if (args.output_reg): print "Printing register contents after simulation."
print "Running simulation for " + str(args.count) + " cycles."
print ""

# Find group file
IN_BASE = "in"
OUT_BASE = "out"
(dirpath, basename, ext) = FileHandler.find_group_file(IN_BASE)
if (dirpath is None or basename is None or ext is None):
	bcolors.print_error("File for group" + str(args.group) + "-" + str(args.lab_name) + " not found.")
	sys.exit()

# Unpack the archive
bcolors.print_header( "Unpacking archive" )

out_dir  = OUT_BASE+"/"+"group"+str(args.group)+"-"+args.lab_name
archive_name = dirpath+"/"+basename+ext
FileHandler.create_dir( OUT_BASE, out_dir )
ret_val = Unpacker.unpack(archive_name, out_dir)
if (not ret_val):
	# TODO: This could be some sort of utility function.
	bcolors.print_ok( "Archive unpacked." )
else:
	bcolors.print_error("Problem while unpacking.")
	sys.exit(-1)
print ""

# Find a relevant mips_program.objdump
bcolors.print_header("Locating objdump")
if   (args.ext ): program_name_allowed = ["mips_ext_program.objdump", "mips_pipe_extended_program.objdump"]
elif (args.pipe): program_name_allowed = ["mips_pipe_program.objdump"]
else            : program_name_allowed = ["mips_program.objdump"]

program_path = None
for program_name in program_name_allowed:
	program_path = FileHandler.find_relative_path( out_dir, program_name )
	if (program_path is None):
		continue
	else:
		program_full_path = program_path + "/" + program_name
		break
if (program_path is None):
	bcolors.print_error( "Missing objdump with name: " + program_name_allowed )
	sys.exit(-1)

bcolors.print_ok_msg("Found objdump at:", program_full_path)
print ""

# Run in syncsim
bcolors.print_header("Running in SyncSim")
syncsim_path = args.syncsim_path;
syncsim_opts = []
syncsim_opts += ["--no-gui", program_full_path]
if   (args.ext ): syncsim_opts += ["--mips-ext" ];
elif (args.pipe): syncsim_opts += ["--mips-pipe"];
else            : syncsim_opts += ["--mips"];
if (args.output_mem): syncsim_opts += ["--output-mem"];
if (args.output_reg): syncsim_opts += ["--output-reg"];
if (args.output_ow ): syncsim_opts += ["--output-ow" ];
syncsim_opts += ["-c", str(args.count)];
java_path    = "java"
java_opts    = ["-jar", syncsim_path]
java_cmd     = [java_path] + java_opts + syncsim_opts
print "Invoking " + " ".join(java_cmd)
subprocess.call( java_cmd )
print ""

# Done, kthx bye!
