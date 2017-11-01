########################################################################
# Imports
#######################################################################

import imp
import os

from subprocess import Popen, PIPE, call as subproc_call
from xtf_error import XTFError

########################################################################
# Classes
#######################################################################

class XLDomain(object):
    """ XEN Domain using the XL toolstack """

    def __init__(self, config_file):
        self.__config_file = config_file
        code = open(config_file)
        self.__config = imp.new_module(config_file)
        exec code in self.__config.__dict__
        self.console = None

    def __RunCmd(self, args):
        p = Popen(args, stdout = PIPE, stderr = PIPE)
        _, stderr = p.communicate()
        return p.returncode, _, stderr

    def __XLCreate(self):
        args = ['xl', 'create', '-p', self.__config_file]
        ret, _, stderr = self.__RunCmd(args)
        if ret:
            raise XTFError("XLDomain.Create", ret, _, stderr)

    def __DomID(self):
        args = ['xl', 'domid', self.__config.name]
        ret, _, stderr = self.__RunCmd(args)
        if ret:
            raise XTFError("XLDomain.DomID", ret, _, stderr)
        return long(_)

    def __Unpause(self):
        args = ['xl', 'unpause', str(self.__domid)]
        ret, _, stderr = self.__RunCmd(args)
        if ret:
            raise XTFError("XLDomain.Unpause", ret, _, stderr)

    def Create(self):
        self.__XLCreate()
        self.__domid = self.__DomID()
        args = ['xl', 'console', str(self.__domid)]
        self.console = Popen(args, stdout = PIPE, stderr = PIPE)

    def Start(self):
        self.__Unpause()

    def Wait(self):
        _, stderr = self.console.communicate()
        if self.console.returncode:
            raise XTFError("XLDomain.Console", self.console.returncode,
                    _, stderr)

        return _
