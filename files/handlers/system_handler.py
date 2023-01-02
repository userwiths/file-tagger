import uuid,os, sys,subprocess

from core import FileHandler
class FileHandler(FileHandler):
    """
    This class is meant to function as an abstraction for actions upon files.
    This current version allows the execution of a command in the system shell with the file passed as argument.
    """
    def __init__(self, command="start", arguments=""):
        self.shell_command=command
        self.shell_arguments=arguments

    def handle(self, path:str):
        """
        Upon a given 'path' to a file, either apply logic for different types of files or directly execute operation.
        """
        try:
            retcode = subprocess.call(' '.join([self.shell_command,self.shell_arguments,path]), shell=True)
            if retcode < 0:
                print("Child was terminated by signal "+ str(-retcode))
            else:
                print("Child returned "+ str(retcode))
        except OSError:
            print("Execution failed:")
