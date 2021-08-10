import uuid,os, sys,subprocess

class FileHandler:
    def __init__(self,command="start",arguments=""):
        self.shell_command=command
        self.shell_arguments=arguments

    def handle(self,path):
        try:
            retcode = subprocess.call(' '.join([self.shell_command,self.shell_argument,path]), shell=True)
            if retcode < 0:
                print("Child was terminated by signal "+ str(-retcode))
            else:
                print("Child returned "+ str(retcode))
        except OSError:
            print("Execution failed:")
