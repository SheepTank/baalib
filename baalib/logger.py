from termcolor import colored as coloured
from datetime import datetime as dt
from dateutil import tz
from typing import Optional
import traceback
import inspect

class Logger():
    def __init__(self, debug:bool=True, verbose:bool=True, write:bool=False, **kwargs):
        self.verbose = verbose
        self._debug  = debug
        self.write   = write
        self.kwargs  = kwargs
        self.logName = kwargs.get("logName") if kwargs.get("logName") is not None else "log.baalib"
        
        self.tz        = tz.gettz(kwargs.get("tzinfo")) if kwargs.get("tzinfo") else None
        self.timestamp = self.kwargs.get("timestamp") if self.kwargs.get("timestamp") else True

    def _getTimestamp(self, timestamp):
        if not timestamp:
            return f""
    
        if self.tz is None:
            return f"[{dt.utcnow().ctime()}] "
        else:
            return f"[{dt.now(tz=self.tz).ctime()}] "

    def _createLog(self, **kwargs) -> Optional[str]:

        logType    = kwargs.get("logType")
        logMessage = kwargs.get("logMessage")

        logTypes = {
            "info":   "[-]", "warn":   "[w]", "success":"[+]",
            "error":  "[!]", "fatal":  "[!]", "debug":  "[D]"
        }

        termColours = {
            "error": {"color": "red"},
            "info": {"color":None, "attrs":[]},
            "success": {"color": "green", "attrs": ["dark"]},
            "debug": {"color": "cyan"},
            "warn": {"color": "yellow"},
            "fatal": {"color": "red", "attrs": ["reverse"]}
        }

        details = {
            "timestamp": [kwargs.get("timestamp"), self.timestamp],
            "write"    : [kwargs.get("write"), self.write],
            "debug"    : [kwargs.get("debug"), self._debug],
            "verbose"  : [kwargs.get("verbose"), self.verbose]
        }

        write     = details["write"][0] or details["write"][1]
        debug     = details["debug"][0] or details["debug"][1]
        verbose   = details["verbose"][0] or details["verbose"][1]
        timestamp = details["timestamp"][0] or details["timestamp"][1]

        end = kwargs.get("end") or "\n"
        entry = " ".join([self._getTimestamp(timestamp)+logTypes[logType], logMessage])
        if "traceback" in kwargs:
            entry+="\n"+kwargs["traceback"]

        colouredEntry = coloured(entry, **termColours[logType])

        if write:
            open(self.logName,"a").write(entry+"\n")
        if logType != "debug" and verbose:
            print(colouredEntry, end=end)
        if logType == "debug" and debug:
            print(colouredEntry, end=end)

    def log(self, logMessage, **kwargs):
        kwargs = {"logType":"info", "logMessage":logMessage, **kwargs}
        self._createLog(**kwargs)
    
    def warn(self, logMessage, **kwargs):
        kwargs = {"logType":"warn", "logMessage":logMessage, **kwargs}
        self._createLog(**kwargs)
    
    def success(self, logMessage, **kwargs):
        kwargs = {"logType":"success", "logMessage":logMessage, **kwargs}
        self._createLog(**kwargs)
    
    def error(self, logMessage, **kwargs):
        kwargs = {"logType":"error", "logMessage":logMessage, **kwargs}
        self._createLog(**kwargs)
    
    def fatal(self, logMessage, **kwargs):
        kwargs = {"logType":"fatal", "logMessage":logMessage, **kwargs}
        self._createLog(**kwargs)

    def debug(self, logMessage, **kwargs):
        callingFrame = inspect.currentframe().f_back
        functionName = callingFrame.f_code.co_name
        lineNumber = callingFrame.f_lineno
        kwargs = {"logType":"debug", "logMessage":f"({functionName}:{lineNumber}) {logMessage}", **kwargs}
        self._createLog(**kwargs)

    def traceback(self, function):
        def wrapper(*args, **kwargs):
            try: function(*args, **kwargs)
            except Exception as e: self._createLog(**{"logType":"error", "logMessage":str(e)+f"\nPositional Arguments: {repr(args)}, Keyword Arguments: {repr(kwargs)}"+"\n"+traceback.format_exc()})
        return wrapper