#!/usr/bin/python3
# -*- coding: utf-8 -*-
#=============================================================
# Created: Tue 26 Oct 2021 03:26:17 PM -03
# Modified: Fri 24 Mar 2023 10:35:26 AM -03
# Description: Checks communication delay on a given port.
# Autor: Leonardo Berbert Gomes
#=============================================================


import sys
import socket
import time
import signal
import logging
from timeit import default_timer as timer
import telegram,telegram_send,os
from logging.handlers import TimedRotatingFileHandler

host = None
port = 80

# Default to 10000 connections max
maxCount = 10000
count = 0

## Inputs

# Required Host
try:
    host = sys.argv[1]
except IndexError:
    print("Usage: network_delay.py host [port] [maxCount]")
    sys.exit(1)

# Optional Port
try:
    port = int(sys.argv[2])
except ValueError:
    print("Error: Port Must be Integer:", sys.argv[3])
    sys.exit(1)
except IndexError:
    pass

# Optional maxCount
try:
    maxCount = int(sys.argv[3])
except ValueError:
    print("Error: Max Count Value Must be Integer", sys.argv[3])
    sys.exit(1)
except IndexError:
    pass

# Pass/Fail counters
passed = 0
failed = 0

getpid=os.getpid()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
scriptname = sys.argv[0].split('/')[-1].split('.')[0]
handler=TimedRotatingFileHandler('logs/' + scriptname + '_' + host + '.log', when="midnight", backupCount=10)
formatter=logging.Formatter('%(asctime)s - PID=' + str(getpid) + ' - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def TelegramMessage(message):
    logger.info('Starting connection with Telegram ...')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex(('api.telegram.org',443))

    if result == 0:
        try:
            logger.info('Open connection, sending message ...')
            logger.info('Send Telegram Mensage: ' + str(message))
            telegram_send.send(messages=[u'\U000026A0 '+str(message)])
        except telegram.error as e:
            logger.error(e)
    else:
        logger.error('Unable to send your message, check your connection with the telegram ...')

def getResults():
    myhost = host
    lRate = 0
    if failed != 0:
        lRate = failed / (count) * 100
        lRate = "%.2f" % lRate

    #Check perc grant 30%
    if float(lRate) > 30:
        diff = (passed - failed)
        message = ("TCP Ping Results for " + str(myhost) + ": Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format((count), diff, failed, str(lRate)))
        TelegramMessage(message)
        logger.error(message)
    else:
        message = ("TCP Ping Results for " + str(myhost) + ": Connections (Total/Pass/Fail): [{:}/{:}/{:}] (Failed: {:}%)".format((count), passed, failed, str(lRate)))
        logger.info(message)

def signal_handler(signal, frame):
    """ Catch Ctrl-C and Exit """
    getResults()
    sys.exit(0)

# Register SIGINT Handler
signal.signal(signal.SIGINT, signal_handler)

# Loop while less than max count or until Ctrl-C caught
while count < maxCount:

    # Increment Counter
    count += 1

    success = False

    # New Socket
    s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)

    # 1sec Timeout
    s.settimeout(1)

    # Start a timer
    s_start = timer()

    # Try to Connect
    try:
        s.connect((host, int(port)))
        s.shutdown(socket.SHUT_RD)
        success = True
    
    # Connection Timed Out
    except socket.timeout:
        logger.error("Connection timed out!")
        failed += 1
    except OSError as e:
        logger.error("OS Error:", e)
        failed += 1

    # Stop Timer
    s_stop = timer()
    s_runtime = "%.2f" % (1000 * (s_stop - s_start))

    if success:
        logger.info("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (host, port, (count-1), s_runtime))
        passed += 1
        #check delay > 2s (2000 ms)
        if float(s_runtime) > 2000:
            failed += 1
            logger.error("Connected to %s[%s]: tcp_seq=%s time=%s ms" % (host, port, (count-1), s_runtime))
    #print(passed,s_runtime)

    # Sleep for 1sec
    if count < maxCount:
        time.sleep(1)
# Output Results if maxCount reached
getResults()
