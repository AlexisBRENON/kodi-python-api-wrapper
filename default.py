import sys
import os
import xbmc

def main(argc, argv):
    os.mkdir("/tmp/xbmcwrapper")
    os.mkfifo("/tmp/xbmcwrapper")
    pipe = open("/tmp/xbmcwrapper/input_cmd", 'r')
    output = open("/tmp/xbmcwrapper/output", 'w')

    while True:
        line = pipe.readline()
        if line == "exit\n":
            break
        else:
            output.write(eval(line))
    return 0

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
