"""
Main module for the PythonWrapper XBMC/Kodi script
"""
import os
import sys
try:
    import xbmc
except ImportError:
#    LOG = print
    pass
else:
    LOG = xbmc.log

def main():
    """ main """
    LOG("### Python wrapper ### Hello !")
    try:
        os.mkdir("/tmp/xbmcwrapper")
    except OSError:
        pass
    try:
        os.mkfifo("/tmp/xbmcwrapper/input_cmd")
    except OSError:
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
                LOG("### Python wrapper ### {0}".format(cmd.strip()))
                if cmd.startswith("eval\n"):
                    cmd = cmd.replace("eval\n", "", 1)
                    output.write("Executing '''\n{}\n'''\n".format(cmd.strip().replace("\n",
                        "\n  ")))
                    exec_globals = globals()
                    sys_stdout = sys.stdout
                    exec_globals['sys'].stdout = output
                    exec(cmd, exec_globals)
                    exec_globals['sys'].stdout = sys_stdout
                    output.write("Execution done.\n\n")
                else:
                    try:
                        returned = eval(cmd, globals())
                    except Exception as eval_exception:
                        returned = "Exception raised during evaluation : {0}".format(eval_exception)
                    output.write("Input : < {0} >\n\tReturned : < {1} >\n\n".format(cmd.strip(),
                        returned))
                output.flush()

    os.unlink("/tmp/xbmcwrapper/input_cmd")
    return 0

if __name__ == "__main__":
    main()
