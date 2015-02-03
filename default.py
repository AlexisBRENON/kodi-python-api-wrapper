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
    except FileExistsError:
        pass
    try:
        os.mkfifo("/tmp/xbmcwrapper/input_cmd")
    except FileExistsError:
        pass

    abort = False
    with open("/tmp/xbmcwrapper/output", 'a') as output:
        LOG("### Python wrapper ### File opened !")
        while not abort:
            pipe = open("/tmp/xbmcwrapper/input_cmd", "r")
            cmd = ''.join(pipe.readlines())
            pipe.close()
            if cmd == "exit\n":
                LOG("### Python wrapper ### Exiting")
                abort = True
            else:
                if cmd.startswith("eval\n"):
                    cmd = cmd.replace("eval\n", "", 1)
                    exec(cmd)
                else:
                    LOG("### Python wrapper ### {0}".format(cmd.strip()))
                    try:
                        returned = eval(cmd, {"sys.stderr" : output})
                    except Exception as eval_exception:
                        returned = "Exception raised during evaluation : {0}".format(eval_exception)
                    output.write("Input : < {0} >\n\tReturned : < {1} >\n\n".format(cmd.strip(),
                        returned))
                    output.flush()

    os.unlink("/tmp/xbmcwrapper/input_cmd")
    return 0

if __name__ == "__main__":
    main()
