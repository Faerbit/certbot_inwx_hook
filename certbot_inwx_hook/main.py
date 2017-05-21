#!/usr/bin/env python3

import os
import sys
import traceback
from time import sleep
from signal import signal, SIGCHLD, SIGINT
from .constants import CERTBOT_DOMAIN_ENV, CERTBOT_VALIDATION_ENV
from .inwx_challenge import InwxChallenge

def get_pid_file_path(domain):
    domain = domain.replace(".", "_")
    return (f"/tmp/certbot_inwx_hook_{domain}")

def exit_handler(signum, frame):
    if (signum == SIGCHLD):
        exit()
    if (signum == SIGINT):
        exit(1)

def child():
    try:
        domain = os.environ.get(CERTBOT_DOMAIN_ENV)
        validation = os.environ.get(CERTBOT_VALIDATION_ENV)
        InwxChallenge(domain, validation).deploy_challenge()
        with open(get_pid_file_path(domain), "w") as pid_file:
            pid_file.write(str(os.getpid()))
        os.kill(os.getppid(), SIGCHLD)
        # wait 3 minutes before automatic cleanup
        signal(SIGCHLD, exit_handler)
        sleep(3 * 60)
    except SystemExit:
        os.kill(os.getppid(), SIGINT)
    except:
        traceback.print_exc()
        os.kill(os.getppid(), SIGINT)

def parent():
    # wait for child to finish work, to prevent premature exit
    signal(SIGINT, exit_handler)
    signal(SIGCHLD, exit_handler)
    sleep(20 * 60)
    print("Error: Child process did not return", file=sys.stderr)
    exit(1)

def deploy():
    """Deploys INWX challenge"""
    # fork so that the child can automatically cleanup
    pid = os.fork()
    if pid == 0:
        child()
    else:
        parent()

def cleanup():
    """Cleans INWX challenge"""
    domain = os.environ.get(CERTBOT_DOMAIN_ENV)
    with open(get_pid_file_path(domain)) as pid_file:
        pid = int(pid_file.read().strip)
    os.kill(pid, SIGCHLD)
