import logging
from datetime import datetime
from . import Scrapper, Register

logger = logging.getLogger(__name__)

class Globo(Scrapper):
    URL = "https://oglobo.globo.com/"
    NAME = "O Globo"
    ABBR = "oglobo"

    def parse_main_headline(self):
        section = 'main_headline'
        date = datetime.now()
        registers = []

        logger.info("Getting main_headline")
        try:
            container = self.parser.find('div', class_="template-manchete-destaques-home-container")
            head_containers = container.find_all('section', class_="drop-in-highlight")
            for head_c in head_containers:
                tag = head_c.find('span', class_="hat").string.strip()
                url_container = head_c.find("a", class_="title-anchor")
                url = url_container['href']
                headline = url_container.h2.string.strip()
                try:
                    subheadline = head_c.find('span', class_='subtitle').string.strip()
                except AttributeError:
                    subheadline = ''
                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))

                # TODO: get related
                section = "main_headline_related"
                related_news = container.find_all('div', class_="manchete_bullets__item")
                for r in related_news:
                    tag = r.find('span').string.strip()
                    url = r.find('a').string.strip()
                    headline = r.find('h2').string.strip()
                    subheadline = ''
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
            items = self.parser.find_all('div', class_="highlight")
            for item in items:
                if 'ads' in item['class']: continue
                subheadline = ''
                tag = item.find('h3', class_="highlight__hat").string.strip()
                url_container = item.find('h2', class_='highlight__title')
                url_container = url_container.find('a')
                url = url_container['href']
                headline = url_container.string.strip()
                subheadline_container = item.find('p', class_='highlight__subtitle')
                if subheadline_container:
                    subheadline = subheadline_container.a.string.strip()

                registers.append(Register(url, self.NAME, headline, subheadline, section, '', tag, date))
        except Exception as e:
            logger.warn('Couldn\'t parse headline', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers

    def parse_highlights(self):
        section = 'headline'
        date = datetime.now()
        registers = []

        logger.info("Getting highlights")
        try:
            items = self.parser.find_all('div', class_="item-franja-destaques-home-oglobo")
            for item in items:
                if 'conteudo-de-marca' in item['class']: continue
                tag = item.find('div', class_="highlight__hat").string.strip()
                url_container = item.find('h2', class_='highlight__title')
                url_container = url_container.find('a')
                url = url_container['href']
                headline = url_container.string.strip()
                registers.append(Register(url, self.NAME, headline, '', section, '', tag, date))
        except Exception as e:
            logger.debug(item)
            logger.warn('Couldn\'t parse headline', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers

    def parse_columnists(self):
        section = 'headline'
        date = datetime.now()
        registers = []

        logger.info("Getting columnists")
        try:
            items = self.parser.find_all('div', class_="franja-colunistas__item")
            for item in items:
                tag = item.find('div', class_="franja-colunistas__hat").string.strip()
                url_container = item.find('h2', class_='franja-colunistas__title')
                url_container = url_container.find('a')
                url = url_container['href']
                headline = url_container.string.strip()
                registers.append(Register(url, self.NAME, headline, '', section, '', tag, date))
        except Exception as e:
            logger.warn('Couldn\'t parse headline', exc_info=True)

        logger.info("\u21B3 Results: '%d'", len(registers))
        return registers


    def parse_all(self):
        registers = []
        
        registers.extend(self.parse_main_headline())
        registers.extend(self.parse_news())
        registers.extend(self.parse_columnists())
        registers.extend(self.parse_highlights())

        return registers