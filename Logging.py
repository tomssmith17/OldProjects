### Logging ###
#write status messages to a file
#what parts of your code have executed and what problems have arrisen
#The 5 default levels are Debug(10), Info(20), Warning(30), Error(40), Critical(50)

import logging
import math

#Create and configure logger
#basicConfig: default log level is Warning = 30, all below this won't be logged if left as default
#log file is created in append mode by default, so each new run will add to the output file and not overwrite it
LogFormat = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "C:\\Users\\tomss\\Desktop\\Python Learning Summer 2018\\OutputLogfile.log",
                    level = logging.DEBUG,
                    format = LogFormat,
                    filemode = 'w')
logger = logging.getLogger()   #root logger, has no name
                    
#Test the logger
"""
logger.debug("This is a harmless debug message.")
logger.info("Just some useful info.")
logger.warning("I'm sorry, but I can't do that, Dave.")
logger.error("Did you just try to divide by zero?")
logger.critical("The entire internet is down!!!")
"""

#print(logger.level)

def quadratic_formula(a, b, c):
    #Return the solutions to the equation ax^2 + bx + c = 0
    logger.info("quadratic_formula({0}, {1}, {2})".format(a, b, c))

    #Compute the discriminant
    logger.debug("# Compute the discriminant")
    disc = b**2 - 4*a*c

    #Compute the two roots
    logger.debug("# Compute the two roots")
    root1 = (-b + math.sqrt(disc)) / (2*a)
    root2 = (-b - math.sqrt(disc)) / (2*a)

    #Return the roots
    logger.debug("# Return the roots")
    return (root1, root2)

roots = quadratic_formula(1, 0, 1)
print roots
