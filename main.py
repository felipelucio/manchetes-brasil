import os
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data")
ERROR_PATH = os.path.join(BASE_DIR, "logs")

import logging
import logging.config
import logger_conf
logging.config.dictConfig(logger_conf.LOGGING_CONF)
logger = logging.getLogger(__name__)

import json
from dataclasses import asdict
from datetime import date, datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen

from sites import Register
from sites.estadao import Estadao
from sites.folha_sp import FolhaSP
from sites.globo import Globo


# logging.basicConfig(level=logging.DEBUG)

SITES = [
    Estadao,
    FolhaSP,
    Globo
]

class Database:
    def __init__(self, site):
        self.site = site
        self.db_path = None
        self.registers = []
        self.last_update = None
        self.indent_output = None
        self.show_register = False

    def set_output_indent(self, spaces=2):
        self.indent_output = spaces

    def set_show_register(self, show=True):
        self.show_register = show

    def register(self, register:Register):
        # check if this register is already saved
        if not self.is_registered(register):
            # if nothing was found, register it
            self.registers.append(register.__dict__)
            if self.show_register:
                logger.info("%s | %s", register.headline, register.url)
            return True

        return False

    def is_registered(self, register:Register):
        for r in self.registers:
            if r['url'] == register.url:
                #logger.debug('Already registered: {}'.format(r['url']))
                # TODO: check if it needs update
                return True
        return False

    def register_all(self, registers:list[Register]):
        registered = []
        for r in registers:
            is_new = self.register(r)
            if is_new:
                registered.append(r)
        
        return registered


    def open_db(self, db_path):
        self.db_path = db_path
        
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                data = json.load(file)
                self.last_update = data['last_update']
                self.registers = data['registers']
        
    def save_db(self):
        if self.db_path:
            data_dir = os.path.dirname(self.db_path)
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)

            data_obj = {
                'site': self.site,
                'last_update': datetime.now(),
                'registers': self.registers
            }
            with open(self.db_path, 'w') as file:
                json.dump(data_obj, file, indent=self.indent_output, default=str)



def print_debug(results):
    for r in results:
        logger.debug("%s \n\t%s\n\t%s\n\t%s", r.headline, r.subheadline, r.tag, r.url)


if __name__ == "__main__":
    year = date.today().strftime("%Y")
    logger.info('Running')

    for site in SITES:
        logger.info("Parsing '%s' registers", site.ABBR)
        http_request = urlopen(site.URL)
        html = http_request.read().decode("utf-8")
        parser = BeautifulSoup(html, "html.parser")
        scrapper = site(parser)
        results = scrapper.parse_all()
        print_debug(results)
        db = Database(site.NAME)
        # db.set_output_indent()
        # db.set_show_register()
        logger.info("Saving '%s' new registers", site.ABBR)
        db.open_db(os.path.join(DATA_PATH, site.ABBR, '{}_{}.json'.format(site.ABBR, year)))
        new_registers = db.register_all(results)
        logger.info("\u21B3 Total new registers: %d", len(new_registers))
        db.save_db()

        

