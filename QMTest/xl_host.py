########################################################################
# Imports
#######################################################################

from   qm.host import Host
import os
import os.path
from   qm.fields import TextField, SetField
import qm.common
import sys
from xl_domain import XLDomain

########################################################################
# Classes
#######################################################################

class XLHost(Host):
    """A XEN Host accessible via the xl toolstack."""
    def Run(self, path, arguments, environment = None, timeout = -1,
            relative = False):

        executable = XLDomain(timeout)
        return (executable.Run() ,"")
