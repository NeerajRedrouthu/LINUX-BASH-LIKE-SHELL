# LINUX-BASH-LIKE-SHELL
It was in Advanced Operating Systems class. We were asked to create our own bash shell with some built-in bash commands  and additional commands specified by the professor. It was a month long project, though arduous I enjoyed it mainly  because everything worked as expected.

Write a C/C++/Python program that implements your own shell.  It should print a
prompt which is the concatenation of your login id and the char string
"_sh> " (note the blank at the end). So, mine for example would be
"rbutler_sh> " without the quotes.  However, the shell should not print
a prompt if its stdin is not a tty or if it is given a single command-line
arg which is a file to accept commands from instead.  Assume that no
command-line will be more that 64 bytes.

The shell should mimic the operation of other shells when there is any
confusion as to operation, unless otherwise stated.  It should not be
implemented using the system() library function or other such facilities
to make use of existing shells; it should be a stand-alone product.

For ease of parsing, you may assume that all command-line values are
separated by at least one char of white-space and that a single command
is on a single line.  A # anywhere on the line marks the beginning of
a comment and thus the end of the line.

The shell should provide these built-in commands:
   quit (or end-of-file, e.g. cntl-D on tty)
   set var val  (shell variable - not env)
   echo word $shellvar $envvar    # print shellvar if same name exists
   envprt (print the environment)
   envset VAR VAL
   envunset VAR
   witch (like which :)
   lim cputime memory (no args prints current; setrlimit CPU or AS)
       lim takes either 0 args or exactly 2 args, e.g.:
           lim 3 4  # (max of 3 seconds cputime and 4 MB of memory)
   pwd
   cd  (no args -> no change) (one arg may be relative or absolute)
Built-in commands are executed in the shell's process.
Variables can be used on any command-line, but no variable value
can contain a $ that causes recursive variable interpolation.
A valid value on a command-line might be:
    cd $HOME/$nextdir
where both HOME and nextdir must be interpolated.
Valid vars consist of alphas, numerics, and underscore.

The shell should provide these environment variables at start-up:
    AOSPATH (default is /bin:/usr/bin)
    AOSCWD  (current working directory) (cd should cause it to be updated)
And, those two vars should be the ONLY two at start-up.
So, I should be able to immediately execute:
    echo $AOSPATH $AOSCWD

Any command that is not built-in, should be found in the AOSPATH.
Follow the convention of forking a new process for commands that are not
built-in.  Use execve to exec the programs.

Provide this form of command-line execution also:
    pgm1 arg1 arg2 arg3 | pgm2 a1 ax | pgm3 b1 bx

Do *not* bother to provide special support for concepts such as process
groups or sessions, e.g.: (p;q) > out
