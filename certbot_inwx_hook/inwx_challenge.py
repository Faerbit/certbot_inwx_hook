import logging
import time
import traceback
from configparser import ConfigParser
from os import environ, path
from ast import literal_eval

import dns.resolver
import dns.exception

from .inwx import domrobot
from .constants import (DEFAULT_CONFIG_FILE_PATH, CONFIG_OVERWRITE_ENVVAR, 
    API_URL)

logger = logging.getLogger(__name__)

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
                self.debug = config.getboolean("default", "debug",
                        fallback=False)
                self.api = domrobot(API_URL, 
                        debug = self.debug)
                self.api.account.login({
                    "user": config.get("default", "user"),
                    "pass": config.get("default", "password")
                    })
                if "nameservers" in config["default"]:
                    self.nameservers = literal_eval(
                            config.get("default", "nameservers", fallback=[]))
                else:
                    self.nameservers = []
                break
        else:
            logger.error("Please provide a configuration file under "
                    + " or ".join(map(lambda x: "'" + str(x) + "'",
                        config_file_locations)) + ".")
            exit(1)
        self.domain = domain
        self.validation = validation

    def __del__(self):
        if hasattr(self, "recordId") and self.recordId:
            self._clean_challenge()

    def deploy_challenge(self):
        """Creates challenge TXT record"""
        logger.info(f"Creating TXT record for \"{self.domain}\"...")
        tld = ".".join(self.domain.split(".")[-2:])
        name = "_acme-challenge." + self.domain
        response = self.api.nameserver.createRecord({"domain": tld,
            "type": "TXT", "content": self.validation, "name": name})
        recordId = response["resData"]["id"]
        logger.info("TXT record registered...")
        logger.info("Checking if DNS has propagated...")
        for i in range(1, 21):
            if (self._has_dns_propagated() == False and i < 20):
                logger.info(f"Try {i:2}/20 failed: DNS not propagated, "
                    "waiting 30s...")
                time.sleep(30)
            elif (self._has_dns_propagated() == False and i == 20):
                logger.error(f"Try {i:2}/20 failed: DNS not propagated.")
                break
            else:
                break
        logger.info("DNS propagated.")
        return recordId

    def clean_challenge(self):
        """Deletes challenge TXT record"""
        tld = ".".join(self.domain.split(".")[-2:])
        name = "_acme-challenge." + self.domain
        name= ".".join(name.split(".")[:-2])
        response = self.api.nameserver.info({"domain": tld, "name": name})
        record = response["resData"]["record"][0]
        if record["type"] != "TXT":
            logger.error(
                f"Could not find correct record for domain \"{self.domain}\". "
                f"Type mismatch should be \"TXT\", "
                f"but is \"{record['type']}\".")
            return
        if record["content"] != self.validation:
            logger.error(
                f"Could not find correct record for domain \"{self.domain}\". "
                f"Content mismatch should be \"{self.validation}\", "
                f"but is \"{record['content']}\".")
            return
        recordId = record["id"]
        self.api.nameserver.deleteRecord({"id": recordId})
        logger.info(f"Deleted TXT record for \"{self.domain}\".")

    def _has_dns_propagated(self):
        """Checks if the TXT record has propagated."""
        txt_records = []
        name = "_acme-challenge." + self.domain
        try:
            resolver = dns.resolver.Resolver()
            nameservers = self.nameservers
            nameservers.extend(resolver.nameservers)
            resolver.nameservers = nameservers
            dns_response = resolver.query(name, "TXT")
            if hasattr(dns_response.response, "answer"):
                for answer in dns_response.response.answer:
                    for record in answer.items:
                        txt_records.append(record.to_text().replace("\"", ""))
        except dns.exception.DNSException as error:
            if (self.debug):
                traceback.print_exc()
            return False

        for txt_record in txt_records:
            if txt_record == self.validation:
                return True

        return False
