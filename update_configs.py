#/usr/bin/env python3

import sys
import os
import shutil
import difflib

mypath = os.path.dirname(os.path.realpath(__file__))
default_filename = os.path.join(mypath,"settings.txt")
default_configdir = os.path.join(mypath,"configs")


class Command:
    update_target = 0
    update_source = 1
    update_noop= 2
    __update_readable__ = {update_target: "Target",
            update_source: "Source",
            update_noop: "NoOp"}

    def __init__(self, target):
        self.__target__ = target

    def __type_str__(self):
        raise NotImplementedError

    def diff(self):
        raise NotImplementedError

    def __get_file_age__(filename):
        st = os.stat(os.path.expanduser(filename))
        return st.st_mtime


    def target_age(self):
        return Command.__get_file_age__(self.__target__)

    def source_age(self):
        raise NotImplementedError

    def target(self):
        return self.__target__

    def source(self):
        return NotImplementedError

    def update_style(self):
        if len(self.diff()) == 0:
            return self.update_noop
        ta = self.target_age()
        na = self.source_age()

        if ta == na:
            return  Command.update_noop
        elif ta < na:
            return Command.update_target
        else:
            return Command.update_source
    def update_human_readable(self):
        return Command.__update_readable__[self.update_style()]


    def __repr__(self):
        return "{0}:[{1}],{2}".format(self.__type_str__(),self.__target__,self.update_human_readable())


class FileCommand(Command):
    def __type_str__(self):
        return "File"
    def __init__(self,target,args):
        super().__init__(target)
        self.__source__ = os.path.join(default_configdir,args[0])
        #TODO: this only works for text files I think?
        source_lines = open(os.path.expanduser(self.__source__),"r").readlines()
        target_lines = open(os.path.expanduser(self.__target__),"r").readlines()
        self.__diff__ = list(difflib.unified_diff(source_lines,target_lines))

    def diff(self):
        return self.__diff__


    def source_age(self):
        return Command.__get_file_age__(self.__source__)


class GitCommand(Command):
    def __type_str__(self):
        return "Git"
    def diff(self):
        return []
    def __init__(self,target,args):
        super().__init__(target)

    def source_age(self):
        return -1


def make_command(cmd,target,args):
    if cmd == "=":
        return FileCommand(target,args)
    elif cmd == ":git:":
        return GitCommand(target,args)
    else:
        raise Exception("Unknown Command",cmd)




class Settings:
    def __init__(self, lines):
        self.__name__ = lines[0][1:-1]
        print(self.__name__)
        
        #triplets of command, target, command args
        self.__commands__ = [make_command(line[1],line[0],line[2:]) for line in map(lambda x: x.split(), lines[1:])]

    def process(self):
        for cmd in self.__commands__:
            style = cmd.update_style()
            print(cmd)
            if style is not Command.update_noop:
                print("".join(cmd.diff()))

            




def __main__():
    filename = default_filename
    if len(sys.argv) > 1:
        filename = argv[1]
    with open(filename,"r") as f:
        lines = list(filter(lambda x: len(x) > 0,map(lambda x: x.strip(),  f.readlines())))
        print(lines)
        indices = []

        for i,line in enumerate(lines):
            if line[0] == '[':
                indices.append(i)

        indices.append(len(lines))

        settings = [Settings(lines[i:j]) for i,j in zip(indices[:-1],indices[1:])]

        for s in settings:
            s.process()
        




if __name__ == "__main__":
    __main__()

