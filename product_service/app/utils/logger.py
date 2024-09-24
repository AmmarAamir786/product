import logging

#logger is just like print. it is more secure so we will use this to check our logs in the console.
#Helps us debugging errors

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger(__name__)