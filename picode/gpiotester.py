#!/usr/bin/python
import RPi.GPIO as g
import time
import ConfigParser

#
#
# the purpose of this function is the entry point for the software, it loads config variables, starts GPIO before invoking the main loop to scan the ports
def main(configfilename):

    # read the config file into the object
    config = ConfigParser.ConfigParser()
    config.read(configfilename)

    # read the application variables
    startbuttongpiopin = config.getint('general', 'startbuttongpiopin')
    pulsegpiopin = config.getint('general', 'pulsegpiopin')
    
    # setup the GPIO and variables
    g.setmode(g.BCM)
    g.setup(int(pulsegpiopin), g.IN)
    g.setup(int(startbuttongpiopin), g.IN)

    # Wait for the GPIO pin to toggle low button to be pushed
    looping = True
    while looping == True:
        print"startbuttongpiopin[%d]=%s; startbuttongpiopin[%d]=%s" % (
            startbuttongpiopin,
            str(g.input(startbuttongpiopin)),
            pulsegpiopin,
            str(g.input(startbuttongpiopin))
        )
        
        time.sleep(1)
    #while

    # release the GPIO
    g.cleanup()
    
#enddef

#
#
# the purpose of this is to allow the application to be invoked from the commandline and pass sys.argv[1] into main()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("ERROR: You must specify the configuration filename on the command line")
        exit(1)
    else:
        # get the config name from the command line and pass in
        main(sys.argv[1])
    #endif
#endif

#EOF
