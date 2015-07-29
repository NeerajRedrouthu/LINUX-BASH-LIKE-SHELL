#!/usr/local/bin/python
#-----------------------------------------------------------------------------------------------------------
#			Project 3: SHELL
#-----------------------------------------------------------------------------------------------------------
import re
import sys
import os
import resource
import time

def dollar(cmd):
	global output,command,c
	while(len(command)>0):
		if ':' in command[0]:
			command = command[0].split(':')
		if '$' in command[0]:
			cmd = command[0].split('$')
			if '' in cmd:
				cmd.remove('')
			while (len(cmd)>0):
				if cmd[0] in envvar:
					if c == 'envset' and len(cmd)==1:
						output += str(envvar[cmd[0]])
					else:
						if c == 'echo':
							output += str(envvar[cmd[0]])	
						else:
							output += str(envvar[cmd[0]])+":"
				elif cmd[0] in shellvar:
					output += str(shellvar[cmd[0]])
				else:
					output += str(cmd[0])
				cmd.pop(0)
			
		else:
			if c == 'envset' and (len(command)==1):
				output += ":"+str(command[0])
			else:
				output += str(command[0])+":"		
		command.pop(0)


def bi():
	global fo,USER,AOSPATH,AOSCWD,output,prompt,envvar,shellvar,bicmds,command,cmd,cputime,cpumemory,pid,found,c;

	#======= IF its a built-in command
	if command[0] in bicmds:
		if command[0] == 'echo':
			command.pop(0)
			if '$' in command[0]:
				c = 'echo'
				dollar(command)
			else:
				output +=  str(command[0])
			command = []
			print output
			output = ''
			c = ''
	#---------------------------------------------------------------------PWD------------------------------------------------------------(functional)
		elif command[0] == 'pwd':
			output += str(AOSCWD)
			command = []
			print output
			output = ''
	#---------------------------------------------------------------------CD------------------------------------------------------------(functional)
		elif command[0] == 'cd':
			if len(command) == 1:
				os.chdir(str(os.getenv("HOME")))
				AOSCWD = os.getcwd()
			elif '$' in command[1]:
				cmd = command[1]
				command.pop(0)
				dollar(command)
				if os.path.exists(output):
					os.chdir(output)
					output = ''
					AOSCWD = os.getcwd()
				else:
					output =''
					output += str(command[0])+': '+str(command[1])+": No such file or directory"
					print output
			elif command[1] == '~':
				os.chdir(str(os.getenv("HOME")))
				AOSCWD = os.getcwd()

			else:		
				if os.path.exists(command[1]):
					os.chdir(command[1])
					AOSCWD = os.getcwd()
				else:
					output =''
					output += str(command[0])+': '+str(command[1])+": No such file or directory"
					print output
			command = []
			output = ''
	#---------------------------------------------------------------------ENVPRINT------------------------------------------------------------(functional)
		elif command[0] == 'envprt':
			l = envvar.items()
			for n,i in enumerate(l):
				if n != len(l)-1:
					output += str(i[0])+'='+str(i[1])+'\n'
				else:
					output += str(i[0])+'='+str(i[1])
			command = []
			print output
			output = ''
	#---------------------------------------------------------------------ENVSET------------------------------------------------------------(functional)
		elif command[0] == 'envset':
			if command[1] not in envvar:
				envvar[command[1]] = command[2]
			else:
				
				cmd = command[1]
				command.pop(0)
				command.pop(0)
				
				if '$' in command[0]:
					c = 'envset'			
					dollar(command)
					envvar[cmd]= output
			command = []
			output = ''
			c=''
	#---------------------------------------------------------------------ENVUNSET------------------------------------------------------------(functional)
		elif command[0] == 'envunset':
			if command[1] in envvar:
				del envvar[command[1]]
			command = []
	#---------------------------------------------------------------------SET------------------------------------------------------------(functional)
		elif command[0] == 'set':
			if command[1] not in shellvar:
				shellvar[command[1]] = command[2]
			else:
				cmd = command[1]
				command.pop(0)
				command.pop(0)
				if '$' in command[0]:
					dollar(command)
					shellvar[cmd] = output
			command = []
			output = ''
		
	#---------------------------------------------------------------------WITCH------------------------------------------------------------(functional)
		elif command[0] == 'witch':
			command.pop(0)
			cmd = command
			path = envvar['AOSPATH'].split(':')
			for p in path:
				exc = os.listdir(p)
				for v in cmd:
					if v in exc:
						output += str(p)+'/'+v 
						command.pop(0)
			print output
		
			command = []
			output = ''
	#---------------------------------------------------------------------LIM------------------------------------------------------------(functional)
		elif command[0] == 'lim':
			command.pop(0)
			if len(command) == 0:
				print "CPU Time:",cputime
				print "CPU Memory:",cpumemory
			elif len(command) == 2:
				cputime = command[0]
				cpumemory = command[1]
				resource.setrlimit(resource.RLIMIT_CPU,(int(cputime),int(cputime)))
				resource.setrlimit(resource.RLIMIT_CORE,(int(cpumemory),int(cpumemory)))
			command = []
			output = ''	#change here
	#---------------------------------------------------------------------QUIT------------------------------------------------------------(functional)			
		elif command[0] == 'quit':
			command = []
			sys.exit(0)	
		
def nbi(cmds):
	global fo,USER,AOSPATH,AOSCWD,output,prompt,envvar,shellvar,bicmds,command,cmd,cputime,cpumemory,newpid,found,pipes,processes,PI_LIST,PR_LIST,pid,string
	cmd = cmds
	path = envvar['AOSPATH'].split(':')

	#print cmd
	#print envvar
	if pipes == 0:
		for dir in path:
			#print dir
			exc = os.listdir(dir)
			if len(cmd)>0:
				if cmd[0] in exc:
					found = 1
					dir = dir+'/'+cmd[0]
					os.execve(dir,cmd,envvar)
					cmd = []
				command = [] 
	else:
		cmd = cmd.split()
		if pid == 1:
			os.dup(0)
			os.dup2(PI_LIST[0][1],1)		#dup stdout of the process with the pipe's write
			os.close(PI_LIST[0][0])
			os.close(PI_LIST[1][0])
			os.close(PI_LIST[1][1])		
		if pid == 2:
			os.dup2(PI_LIST[0][0],0)		#dup stdout of the process with the pipe 1's read
			os.close(PI_LIST[0][1])
			os.close(PI_LIST[1][0])
			if pipes > 1:
				os.dup2(PI_LIST[1][1],1)	#dup stdout of the process with the pipe 2's write
			else:
				os.close(PI_LIST[1][1])			#else close it
				os.dup(1)
		if pid == 3:
			os.close(PI_LIST[0][0])
			os.close(PI_LIST[0][1])
			os.close(PI_LIST[1][1])
			os.dup2(PI_LIST[1][0],0)		#dup stdout of the process with the pipe 2's read
			os.dup(1)
		for dir in path:
			exc = os.listdir(dir)
			if cmd[0] in exc:
				found = 1
				dir = dir+'/'+cmd[0]
				os.execve(dir,cmd,envvar)

			else:
				os._exit(0)

def parent():
	global argm,fo,USER,AOSPATH,AOSCWD,output,prompt,envvar,shellvar,bicmds,command,cmd,cputime,cpumemory,newpid,found,pipes,processes,PI_LIST,PR_LIST,pid,string
	while True:
		command = []
		pid = 0
		pipes = 0
		processes = 0
		if newpid > 0:
			try:			
				if sys.stdin.isatty() == True:			#input from terminal

					if (len(argm)>1):
						fo = open(argm[1],'r')
						sys.stdin = fo
						command += raw_input().split()
					else:
						command += raw_input(prompt).split()
				else:							#input from a file	
					command += raw_input().split()
			except EOFError:
				sys.exit(0)	
		
		if len(command)>0:
			if command[0] in bicmds:
				if newpid > 0:
					bi()
			else:
				if '|' not in command:	
					for i in range(0,1):
						newpid = os.fork()
						if newpid == 0:
							break
					if newpid == 0:
						nbi(command)
					if newpid>0:
						os.wait()
					
				else:
					for n,cm in enumerate(command):
						if cm == '|':
							pipes+=1
							processes+=1
						if n == len(command):
							string += cm
						else:
							string += cm+' '
					command = string.split('|')
					
					
					for i in range(0,pipes+1):
						newpid = os.fork()
						if newpid == 0:
							pid = i+1
						if newpid == 0:
							break
					
					if newpid == 0:
						nbi(command[pid-1])				
						print "exit from child process:",pid
						
					os.wait()

					
c = ''
string = ''
PI_LIST = []
PR_LIST = [0,0,0]
pid = 0
processes = 1
pipes = 0
USER = os.environ['USER']
AOSPATH = '/bin:/usr/bin'
AOSCWD = os.getcwd()
output = ''
prompt = USER+'_sh> '
envvar = {'AOSPATH':AOSPATH,'AOSCWD':AOSCWD}
shellvar = {'USER':USER}
bicmds = ['quit','set','echo','envprt','envset','envunset','witch','lim','pwd','cd']
command = []
cmd = []
cputime = 0
cpumemory = 0
found = 0
newpid = os.getpid()
for pi in range(0,2):
	PI_LIST .append(os.pipe())
	

argm = sys.argv
if len(argm)>1:
	file_name = open(argm[1],'r')
	a = file_name.read()
	for f in a.split('\n'):
		if f.find('#')!=-1:
			f=f[:f.find('#')]
		if f.startswith('\t')!=True:    
			f = f.strip('    ')

parent()
