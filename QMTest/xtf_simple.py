########################################################################
# Imports
########################################################################

import qm.common
import os.path
import string
import sys

from qm.test.test import Test
from qm.test.result import Result
from qm.fields import TextField, SetField
from xl_domain import XLDomain
from xtf_utils import XTFError, XTFResult

########################################################################
# Classes
########################################################################

class XTFSimpleTest(Test):

    arguments = [
        qm.fields.TextField(
            name = "conf",
            title = "XL configuration file",
            ),
        ]

    def Run(self, context, result):
        """Run the test."""

        conf_file = os.path.normpath(os.path.expandvars(self.conf))

        if not os.path.isfile(conf_file):
            result.Fail("Invalid Configuration file.", {"file": conf_file});
            return

        try:
            domain = XLDomain(conf_file)
            domain.Create()
            domain.Start()
            output = domain.Wait()

        except XTFError as e:
            e.Annotate(result)
            result.Fail("Error while executing test");
            return

        XTFResult(output, result)
