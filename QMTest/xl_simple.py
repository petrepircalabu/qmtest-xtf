########################################################################
# Imports
########################################################################

import os.path
from   qm.test.test import Test
from   qm.test.result import Result
from   qm.fields import TextField, SetField
import qm.common
import string
import sys

from xl_domain import XLDomain
from xtf_error import XTFError

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

    # All results of a test, keep in sync with C code report.h.
    # Notes:
    #  - WARNING is not a result on its own.
    #  - CRASH isn't known to the C code, but covers all cases where a valid
    #    result was not found.
    all_results = ['SUCCESS', 'SKIP', 'ERROR', 'FAILURE', 'CRASH']

    def __ParseResult(self, output):
        """ Interpret the final log line of a guest for a result """

        if not "Test result:" in output:
            return "CRASH"

        for res in self.all_results:
            if res in output:
                return res

        return "CRASH"

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

        res = self.__ParseResult(output)

        if res == 'SUCCESS':
            result.SetOutcome(Result.PASS, cause = output)
        elif res == 'SKIP':
            result.SetOutcome(Result.UNTESTED, cause = output)
        elif res == 'FAILURE':
            result.SetOutcome(Result.FAIL, cause = output)
        elif res == 'ERROR' or res == 'CRASH':
            result.SetOutcome(Result.ERROR, cause = output)
