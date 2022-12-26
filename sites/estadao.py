import logging
from datetime import datetime
from . import Scrapper, Register

logger = logging.getLogger(__name__)

class Estadao(Scrapper):
    URL = "https://www.estadao.com.br/"
    NAME = "O Estado de São Paulo"
    ABBR = "estadao"

    def parse_main_headline(self):
        section = 'main_headline'
        date = datetime.now()
        registers = []
        
        logger.info("Getting main_headline")
        try:
            container = self.parser.find('div', class_='manchete-especial')
            if container:
                tag = container.find('a', class_='subeditorial-url').string
                head_container = container.find('div', class_='manchete-content')
                url = head_container.contents[1]['href']
                headline = head_container.contents[1].h2.string
                subheadline = head_container.contents[1].p.string
                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))

                related_container = self.parser.find('div', class_='manchete-especial-related-news')
                related = related_container.find_all('div', class_='related-news-item')
                for r in related:
                    url = r.contents[0]['href']
                    headline = r.contents[0]['title']
                    section = 'main_headline_related'
                    registers.append(Register(url, self.NAME, headline, '', section, '', tag, date))
            else:
                container = self.parser.find('div', class_='manchete-dia-a-dia-block-container')
                if not container: 
                    logger.info("Couldn't find: main_headline")
                    return registers

                info_container = container.find('div', class_='info')
                tag = info_container.contents[0].a.string
                url = info_container.contents[1]['href']
                headline = info_container.contents[1].h2.string
                subheadline = info_container.contents[1].p.string
                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))

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
            news_blocks = self.parser.find_all('div', class_='noticia-content-block')
            for n in news_blocks:
                subheadline = ''
                tag = n.contents[0].a.string
                headline = n.contents[1].h2.string
                url = n.contents[1]['href']
                if n.contents[1].div:
                    subheadline = n.contents[1].div.string

                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))
                
                # check if exists bullet news    
                if len(n.contents) == 3:
                    for b in n.contents[2].find_all('a'):
                        bullet_url = b['href']
                        bullet_headline = b.span.string
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
        try:
            editorials_block = self.parser.find_all('a', class_='opiniao-home')
            if editorials_block:
                for ed in editorials_block:
                    if 'more' in ed['class']: continue
                    url = ed['href']
                    headline = ed.h3.string
                    try:
                        subheadline = ed.p.string
                    except AttributeError:
                        subheadline = ''
                    registers.append(Register(url, self.NAME, headline, subheadline, section, '', '', date))
        except Exception as e:
            logger.debug(ed)
            logger.warn('Couldn\'t parse editorials', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers



    def parse_all(self):
        registers = []

        registers.extend(self.parse_main_headline())
        registers.extend(self.parse_news())
        registers.extend(self.parse_editorials())

        return registers