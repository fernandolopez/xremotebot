'''Utility module'''
import subprocess

def run(*args, **kwargs):
    '''Receives positional arguments with a command to run and this arguments,
    runs the program and returns a tuple with (returncode, stdout, stderr).'''
    stdout = kwargs.get('stdout', subprocess.PIPE)
    stderr = kwargs.get('stderr', subprocess.PIPE)
    sp = subprocess.Popen(args, stdout=stdout, stderr=stderr)
    out, err = sp.communicate()
    return (sp.returncode, out, err)

def runbg(*args):
    '''Receives positional arguments with a command and this arguments and
    runs it in background'''
    sp = subprocess.Popen(args)
    return sp

