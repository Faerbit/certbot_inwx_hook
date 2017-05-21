import logging
import time
from configparser import ConfigParser
from os import environ, path
from sys import stderr

import dns.resolver
import dns.exception

from .inwx import domrobot
from .constants import (DEFAULT_CONFIG_FILE_PATH, CONFIG_OVERWRITE_ENVVAR, 
    API_URL)


class InwxChallenge:

    def __init__(self, domain, validation, 
            config_file = DEFAULT_CONFIG_FILE_PATH):
        config_file_locations = [ config_file ]
        if environ.get(CONFIG_OVERWRITE_ENVVAR):
            config_file_locations.insert(0, 
                    environ.get(CONFIG_OVERWRITE_ENVVAR))
        for cfg_file in config_file_locations:
            if path.isfile(cfg_file):
                config = ConfigParser()
                config.read(cfg_file)
                self.api = domrobot(API_URL, 
                        debug = config.getboolean("default", "debug",
                            fallback=False))
                self.api.account.login({
                    "user": config.get("default", "user"),
                    "pass": config.get("default", "password")
                    })
                self.nameservers = config.get("default", "nameservers")
                break
        else:
            print("Please provide a configuration file under "
                    + " or ".join(map(lambda x: "'" + str(x) + "'",
                        config_file_locations)) + ".", file=sys.stderr)
            exit(1)
        self.domain = domain
        self.validation = validation

    def __del__(self):
        if hasattr(self, "recordId") and self.recordId:
            self._clean_challenge()

    def deploy_challenge(self):
        """Creates challenge TXT record"""
        print("Creating TXT record for {}".format(self.domain))
        tld = ".".join(self.domain.rsplit(".")[-2:])
        name = "_acme-challenge." + self.domain
        response = self.api.nameserver.createRecord({"domain": tld,
            "type": "TXT", "content": self.validation, "name": name})
        self.recordId = response["resData"]["id"]
        print("TXT record registered...")
        if not self.nameservers:
            return
        print("Checking if DNS has propagated...")
        for i in range(20):
            if (self._has_dns_propagated() == False and i < 19):
                print(f"Try {i:2}/20 failed: DNS not propagated, "
                    "waiting 30s...")
                time.sleep(30)
            elif (self._has_dns_propagated() == False and i == 19):
                print(f"Try {i:2}/20 failed: DNS not propagated.",
                        file=sys.stderr)
                break
            else:
                break
        print("DNS propagated.")

    def _clean_challenge(self):
        """Deletes challenge TXT record"""
        self.api.nameserver.deleteRecord({"id":self.recordId})
        print("Deleted TXT record for {}".format(self.domain))

    def _has_dns_propagated(self):
        """Checks if the TXT record has propagated."""
        txt_records = []
        name = "_acme-challenge." + self.domain
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = self.nameservers
            dns_response = resolver.query(name, 'TXT')
            for rdata in dns_response:
                for txt_record in rdata.strings:
                    txt_records.append(txt_record)
        except dns.exception.DNSException as error:
            return False

        for txt_record in txt_records:
            if txt_record == self.validation:
                return True

        return False
