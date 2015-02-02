"""
Main module for the PythonWrapper XBMC/Kodi script
"""
import os
try:
    import xbmc
except ImportError:
    LOG = print
else:
    LOG = xbmc.log

def main():
    """ main """
    LOG("### Python wrapper ### Hello !")
    try:
        os.mkdir("/tmp/xbmcwrapper")
        os.mkfifo("/tmp/xbmcwrapper/input_cmd")
    except FileExistsError:
        pass

    with open("/tmp/xbmcwrapper/input_cmd", 'r') as pipe:
        with open("/tmp/xbmcwrapper/output", 'wa') as output:
            LOG("### Python wrapper ### File opened !")
            while True:
                line = pipe.readline()
                if line == "exit\n":
                    break
                elif len(line) > 0:
                    LOG("### Python wrapper ### {0}".format(line))
                    try:
                        returned = eval(line)
                    except Exception as eval_exception:
                        returned = "Exception raised during evaluation : {0}".format(eval_exception)
                    output.write("Input : < {0} >\n\tReturned : < {1} >\n\n".format(line.strip(),
                        returned))
                    output.flush()
    return 0

if __name__ == "__main__":
    main()
