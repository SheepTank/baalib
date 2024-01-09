from termcolor import colored as coloured  # For colourful messages within terminals
from datetime import datetime as dt  # For timestamp support
from typing import Optional

import traceback  # For traceback support
import inspect    # For additional logger.debug information
import socket     # For remote logging
import json       # For json support

class Logger():
    def __init__(self, debug:bool=True, verbose:bool=True, write:bool=False, json:bool=False, connection:tuple=None, **kwargs):
        self.verbose = verbose
        self._debug  = debug
        self.write   = write
        self.json    = json
        self.logName = kwargs.get("logName") or "log.baalib"
        self.tzinfo  = kwargs.get("tzinfo")
        self.kwargs  = kwargs

        self.timestamp  = kwargs.get("timestamp") or True
        self.connection = connection
        self.socket     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__logTypes = {
            "info":   "[-]", "warn":   "[w]", "success":"[+]",
            "error":  "[!]", "fatal":  "[!]", "debug":  "[D]"
        }

        # Try to connect to the endpoint
        try:
            if self.connection is not None:
                self.socket.connect(self.connection)
        except:
            self.error(f"Failed to connect to specified endpoint. Remote logging unavailable.", traceback=traceback.format_exc())

    def _getTimestamp(self):
        if self.json:
            return f"{dt.utcnow().ctime()}" if self.tzinfo is None else f"{dt.now(tz=self.tzinfo).ctime()}"

        return f"[{dt.utcnow().ctime()}]" if self.tzinfo is None else f"[{dt.now(tz=self.tzinfo).ctime()}]"

    def _createLog(self, **kwargs) -> Optional[str]:

        logType    = kwargs.get("logType")
        logMessage = kwargs.get("logMessage")

        termColours = {
            "error": {"color": "red"},
            "info": {"color":None, "attrs":[]},
            "success": {"color": "green", "attrs": ["dark"]},
            "debug": {"color": "cyan"},
            "warn": {"color": "yellow"},
            "fatal": {"color": "red", "attrs": ["reverse"]}
        }

        write     = kwargs.get("write") if "write" in kwargs else self.write
        debug     = kwargs.get("debug") if "debug" in kwargs else self._debug
        verbose   = kwargs.get("verbose") if "verbose" in kwargs else self.verbose
        timestamp = kwargs.get("timestamp") if "timestamp" in kwargs else self.timestamp
        end       = kwargs.get("end") if "end" in kwargs else "\n"

        if not self.json:
            entry = " ".join([self._getTimestamp(), self.__logTypes[logType], logMessage])
        else:
            entry = {"timestamp":self._getTimestamp(), "type":logType, "value":logMessage}

        if (traceback:=kwargs.get("traceback")) is not None:
            if not isinstance(entry, dict): entry+="\n"+traceback
            else: entry["traceback"] = traceback

        colouredEntry = coloured(entry, **termColours[logType])

        if write:
            open(self.logName,"a").write(entry+"\n")
        
        if not verbose:
            pass
        elif logType == "debug" and not debug:
                pass
        else:
            print(colouredEntry, end=end)

        if self.connection is not None:
            if isinstance(entry, dict):
                entry = json.dumps(entry, indent=4)
            try:
                self.socket.send(f"{entry}\n".encode())
            except:
                self.socket.connect(self.connection)
            finally:
                self.socket.send(f"{entry}\n".encode())

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
