# baalib

## Logger
A custom written logger with some basic debugging features.

### Description
The Logger class (baalib.logger.Logger) started development years ago, because I got bored of print statements. So what did I do? Make more printstatements. Previous iterations of this module had additional functionality which will eventually come back. Features such as webhook support, and debugging functionality which showed roughly where the debug function was called (because `logger.debug("this")` only ever got me so far...)

#### Logger: Features
Once initialised:
```python
from baalib.logger import Logger
logger = Logger(logName='log.baalib', verbose=True, write=True, debug=True)
```
The logger has the following options:
```python
- logger.log('Log message')
- logger.error('Error message')
- logger.fatal('Fatal message')
- logger.debug('Debug message')
- logger.warning('Warning message')
- logger.success('Success message')
```

With example outputs:
```text
[2018-04-18 22:04:49] [-] Log message
[2018-04-18 22:04:49] [!] Error: Error message
[2018-04-18 22:04:49] [F] FATAL: Fatal message
[2018-04-18 22:04:49] [D] Debug: Debug message
[2018-04-18 22:04:49] [W] Warning: Warning message
[2018-04-18 22:04:49] [+] Success: Success message
```

Each of these functions have `verbose` and `write` flags preset.
You can overwrite each of these to further control the logging, an example:

```python
logger.debug('Something happened...')
```
Each function comes with a timestamp by default.
The above would output the following, for example:
```text
[2018-04-18 22:04:49] [D] Debug: Something happened...
```

The logger function comes with some useful switches, is it possible to change the write/verbose/debug values on each individual function by doing:
```python
logger.debug('Something happened...', write=False)
logger.debug('Something happened...', verbose=False)
logger.debug('Something happened...', debug=False)
```

It is further possible to change the output's type, using `logType`:
```python
logger.log('Something happened...', logType='plus')

# Options include:
# plus [+], info [-], error [!], debug [D], warn [W]
```
All Options
```python
logger.log("Log message.", logType="error", write=False, verbose=True, debug=True)
# Options are set to true by default, or defined within the class initialisation.
```

## Networking
A collection of useful functions for networking in python.
