from selenium import webdriver
import time
import pandas as pd
from bs4 import BeautifulSoup


class ScrapeBinanceLaunchpad:

    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        self.launchpad_link = 'https://launchpad.binance.com/en/viewall/lpd'

    @staticmethod
    def split_word(word):
        """

        :param word: word that you want to be splitted
        :return: splitted word
        """
        return [char for char in word]

    def generate_source_page(self, link, options=True):
        """

        :param link: link that you want to generate the source page
        :param options: include optional arguments to selenium
        :return: return the source page to work with bs4
        """
        # Check options
        if options:
            driver = webdriver.Firefox(options=self.options)
        else:
            driver = webdriver.Firefox()
        # Getting the driver
        driver.get(link)
        # Clicking the view buttons to sho the full page
        # TODO: automatizar range de cliques
        for button in range(7):
            click_buttons = driver.find_elements_by_class_name('css-1crqhgr')
            click_buttons[0].click()
            time.sleep(1)
        # Generating and returninf page source
        page_source = driver.page_source
        return page_source

    @staticmethod
    def generate_div_class_html(class_name, page_source):
        """

        :param class_name: html class to scrape
        :param page_source: html source to scrape
        :return: html to extract data
        """
        soup = BeautifulSoup(page_source, 'lxml')
        html = soup.find_all('div', class_=class_name)
        return html

    @staticmethod
    def scrape_token_name(html):
        """

        :param html: html to scrape
        :return: list of launchpad token names
        """
        # ETL the html
        lista_token_names = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) > 5:
                lista_token_names.append(lista_strings[4])
        return lista_token_names[1:]

    @staticmethod
    def scrape_token_offered(html):
        """

        :param html: html to scrape
        :return: list of token offered
        """
        # ETL the html
        lista_token_offered = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) > 5:
                lista_strings_2 = ScrapeBinanceLaunchpad().split_word(lista_strings[1])
                lista_letras = lista_strings_2[7:]
                final_token_offered = "".join(lista_letras)

                lista_token_offered.append(float(final_token_offered[:-5].replace('.', "")))
        return lista_token_offered[1:]

    @staticmethod
    def scrape_sale_price(html):
        """

        :param html: html to scrape
        :return: list of token sale price and compared sale price
        """
        lista_token_price = list()
        lista_token_compared = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) > 5:
                lista_token_price.append(lista_strings[-2])
                lista_token_compared.append(lista_strings[-1])
        return lista_token_price[1:], lista_token_compared[1:]

    @staticmethod
    def scrape_participants(html):
        """

        :param html: html to scrape
        :return: list of participants
        """
        lista_participants = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) == 3:
                lista_strings_2 = ScrapeBinanceLaunchpad().split_word(lista_strings[0])
                lista_letras = lista_strings_2[12:]
                lista_letras = lista_letras[:-5]
                final_participant_list = "".join(lista_letras)
                lista_participants.append(final_participant_list)
            elif len(lista_strings) == 1:
                lista_string = ScrapeBinanceLaunchpad().split_word(lista_strings[0])
                lista_letras = lista_string[12:]
                final_participant_list = "".join(lista_letras)
                lista_participants.append(final_participant_list)
        return lista_participants[1:]

    @staticmethod
    def scrape_total_commited(html):
        """

        :param html: html to scrape
        :return: list of total commited to the launchpad
        """
        lista_total_commited = list()
        lista_token_compared = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) == 3:
                lista_strings_2 = ScrapeBinanceLaunchpad().split_word(lista_strings[-2])
                lista_letras = lista_strings_2[9:]
                final_participant_list = "".join(lista_letras)
                lista_total_commited.append(float(final_participant_list.replace(".", "").replace(",", ".")))
                lista_token_compared.append(lista_strings[-1])
            if len(lista_strings) == 1:
                lista_total_commited.append('Nan')
                lista_token_compared.append('Nan')
        return lista_total_commited[1:], lista_token_compared[1:]

    @staticmethod
    def scrape_end_date(html):
        """

        :param html: html to scrape
        :return: end time offered of the token launch
        """
        lista_end_time = list()
        for item in html:
            lista_strings = item.text.split()
            if len(lista_strings) == 1:
                lista_strings_2 = ScrapeBinanceLaunchpad().split_word(lista_strings[0])
                if '-' in lista_strings_2:
                    lista_end_time.append(lista_strings[0])
        return lista_end_time

    def main_code(self):
        """

        :return: data frame with all the scraped data
        """
        page_source = ScrapeBinanceLaunchpad().generate_source_page(self.launchpad_link)
        html_01 = ScrapeBinanceLaunchpad().generate_div_class_html('css-1wr4jig', page_source)
        html_02 = ScrapeBinanceLaunchpad().generate_div_class_html('css-vurnku', page_source)
        final_dict = {'Token Name': ScrapeBinanceLaunchpad().scrape_token_name(html_01),
                      'Token Ofered': ScrapeBinanceLaunchpad().scrape_token_offered(html_01),
                      'Price': ScrapeBinanceLaunchpad().scrape_sale_price(html_01)[0],
                      'Compared Token Price': ScrapeBinanceLaunchpad().scrape_sale_price(html_01)[-1],
                      'Participants': ScrapeBinanceLaunchpad().scrape_participants(html_01),
                      'Total Commited': ScrapeBinanceLaunchpad().scrape_total_commited(html_01)[0],
                      'Compared Token Commited': ScrapeBinanceLaunchpad().scrape_total_commited(html_01)[1],
                      'End Date': ScrapeBinanceLaunchpad().scrape_end_date(html_02)
                      }
        df = pd.DataFrame(final_dict)
        return df.to_csv('Binance_Launchpad.csv')


if __name__ == '__main__':
    ScrapeBinanceLaunchpad().main_code()
