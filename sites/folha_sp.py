import logging
from datetime import datetime
from . import Scrapper, Register

logger = logging.getLogger(__name__)

class FolhaSP(Scrapper):
    URL = "https://www.folha.uol.com.br/"
    NAME = "Folha de S.Paulo"
    ABBR = "folha_sp"

    def parse_main_headline(self):
        section = 'main_headline'
        date = datetime.now()
        registers = []
        tag = ''
        
        logger.info("Getting main_headline")
        try:
            container = self.parser.find('div', class_='c-main-headline')
            if container:
                try:
                    tag = container.find('div', class_='c-main-headline__head').h3.a.string.strip()
                except AttributeError:
                    tag = container.find('div', class_='c-main-headline__head').h3.string.strip()

                head_container = container.find('a', class_='c-main-headline__url')
                url = head_container['href']
                headline = head_container.h2.string
                subheadline = head_container.p.string
                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))

                related_container = container.find('ul', class_='c-list-links')
                if related_container:
                    related = related_container.find_all('div', class_='c-list-links__content')
                    for r in related:
                        url = r.a['href']
                        headline = r.a.h2.string
                        section = 'main_headline_related'
                        registers.append(Register(url, self.NAME, headline, '', section, '', tag, date))
        except Exception as e:
            logger.warn('Couldn\'t parse main_headline', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers

    def parse_news(self):
        section = 'headline'
        date = datetime.now()
        registers = []
        
        logger.info("Getting news")
        try:
            news_blocks = self.parser.find_all('div', class_='c-headline')
            for n in news_blocks:
                subheadline = ''
                if 'c-headline--opinion' in n['class']:
                    continue
                
                tag_container = n.find('div', class_='c-headline__head')
                if tag_container and tag_container.h3:
                    if tag_container.h3.a:
                        tag = tag_container.h3.a.string.strip()
                    else:
                        tag = tag_container.h3.string.strip()

                head_container = n.find('a', class_='c-headline__url')
                # check if is not a subscribe "headline"
                if not head_container or not head_container.find('h2'):
                    continue

                url = head_container['href']
                try:
                    headline = head_container.h2.text.strip()
                except AttributeError:
                    headline = head_container.text.strip()

                if head_container.p:
                    subheadline = head_container.p.string.strip()
                    
                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))
                
                # check if exists bullet news    
                bullet_list = n.find('ul', class_='c-list-links__url')
                if bullet_list:
                    for b in bullet_list:
                        bullet_url = b['href']
                        bullet_headline = b.contents[2].string.strip()
                        registers.append(Register(bullet_url, self.NAME, bullet_headline, '', section, '', tag, date))
        except Exception as e:
            logger.warn('Couldn\'t parse headline', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers

    def parse_editorials(self):
        section = 'editorial'
        date = datetime.now()
        registers = []

        logger.info("Getting editorials")
        editorials = self.parser.find_all('div', class_='c-headline--opinion')
        for ed in editorials:
            head_container = ed.find('a', class_='c-headline__url')
            url = head_container['href']
            headline = head_container.h2.text.strip()
            try:
                subheadline = head_container.p.text.strip()
            except AttributeError:
                subheadline = ''

            registers.append(Register(url, self.NAME, headline, subheadline, section, '', '', date))

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers

    def parse_all(self):
        registers = []
        
        registers.extend(self.parse_main_headline())
        registers.extend(self.parse_news())
        registers.extend(self.parse_editorials())

        return registers