import subprocess

def run(*args, **kwargs):
    stdout = kwargs.get('stdout', subprocess.PIPE)
    stderr = kwargs.get('stderr', subprocess.PIPE)
    sp = subprocess.Popen(args, stdout=stdout, stderr=stderr)
    out, err = sp.communicate()
    return (sp.returncode, out, err)

def runbg(*args):
    sp = subprocess.Popen(args)
    return sp

