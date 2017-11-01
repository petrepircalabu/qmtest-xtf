########################################################################
# Imports
#######################################################################
class XTFError(Exception):
    def __init__(self, context, error, msg, err_msg):
        self.__context = context
        self.__error = error
        self.__msg = msg
        self.__err_msg = err_msg

    def Annotate(self, result):
        if self.__context:
            label = self.__context + "."
        else:
            label = ""

        if self.__error:
            result.Annotate({label + "error code" : ("%d" % self.__error)})

        if self.__msg:
            result.Annotate({label + "stdout" : result.Quote(self.__msg)})

        if self.__err_msg:
            result.Annotate({label + "stdout" : result.Quote(self.__err_msg)})
