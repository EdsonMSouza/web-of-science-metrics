#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class WoSExtractor:


    def __init__(self, pathChromedriver):

        import warnings
        warnings.simplefilter("ignore")

        import pandas as pd
        import numpy as np
        import time
        import sys
        import re
        import os

        from bs4 import BeautifulSoup

        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.chrome.options import Options

        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        self.driver = webdriver.Chrome(chrome_options=options, executable_path=pathChromedriver)

        url = "https://apps.webofknowledge.com/WOS_GeneralSearch_input.do?product=WOS&search_mode=GeneralSearch&SID=5CyVjJdhzFKByBwwLGr"
        self.driver.get(url)

        # eliminates any open sessions
        self.driver.find_element_by_xpath('//*[@id="signin"]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/div[22]/ul[2]/li[1]/ul/li[3]/a').click()
        self.driver.get(url)

        # language as english
        self.driver.find_element_by_xpath('//html/body/div[1]/div[22]/ul[2]/li[3]').click()
        self.driver.find_element_by_xpath('//html/body/div[1]/div[22]/ul[2]/li[3]/ul/li[3]/a').click()

        # Advanced Search
        self.driver.find_element_by_xpath('//html/body/div[9]/div/ul/li[4]/a').click()
        
        # type of documents: article
        self.driver.find_element_by_xpath("//select/option[@value='Article']").click()
        time.sleep(2)
        self.driver.find_element_by_xpath("//select/option[@value='Article']").click()

        # Focus to field search
        self.elem = self.driver.find_element_by_name("value(input1)")

    # method to print out inline
    def printer(self, data):
        import sys
        import os
        sys.stdout.write("\r\x1b[K" + data.__str__())
        sys.stdout.flush()

    # List requested errors
    def errors(self, l, file):
        arq = open(file + '_log_errors.csv', 'w', encoding='utf-8')
        arq.write('WOS_ID; LINK\n')
        print('\n\nATTENTION:\nSome articles could not be fully extracted!\n(Check log file: ' + file + '_log_errors.csv)\n')
        print('Below are the articles not extracted\n')
        for error in l:
            arq.write(error[0] + ';' + error[1] + '\n')
            print(error[0], error[1][0:50])
        arq.close()

    def getPageCount(self, s):
        return int(s.find('span', {'id': 'pageCount.top'}).text)

    def get_link(self, url_base, s):
        return url_base + s.find('a').get('href')


    # Extract data about authors
    def author_names(self, s):
        author = s.find_all('a', {'title': 'Find more records by this author'})
        names = [name.text for name in author]
        return ('; ').join(names)

    # Extract data year of publication
    def year_publised(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'Published:'):
                    return si.find('value').text.split(' ')[-1]
            except:
                pass

    # Extract data about DOI
    def doi(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'DOI:'):
                    return si.find('value').text
            except:
                pass

    # Extract data about Impact Factor
    def impact_factor(self, s):
        p = s.find_all('table', {'class': 'Impact_Factor_table'})
        for si in p:
            try:
                return [si.findAll('td')[0].string, si.findAll('th')[0].string, si.findAll('td')[1].string]
            except:
                pass

    # Extract data about Abstract
    def abstract(self, s):
        for si in s.find_all('div', {'class': 'block-record-info'}):
            div = si.find('div', {'class': 'title3'})
            if div is not None:
                if div.text == 'Abstract':
                    return si.find('p').text

    # Extract data about References and Citations
    def number_ref_cited(self, s):
        tag_p = s.find_all('p', {'class': 'FR_field'})
        for i, p in enumerate(tag_p):
            tag = p.find_all('a', {'title': "View this record's bibliography"})
            for t in tag:
                if t is not None:
                    try:
                        ref = t.find('b').text
                        try:
                            cited = tag_p[i + 1].find('b').text
                            return ref, cited
                        except:
                            return ref, None
                    except:
                        return None, None

    # Extract data about WoS ID
    def wos_id(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'Accession Number:'):
                    return si.find('value').text
            except:
                pass

    # Extract data about ISSN
    def issn(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'ISSN:'):
                    return si.find('value').text
            except:
                pass

    # Extract data about eISSN
    def e_issn(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'eISSN:'):
                    return si.find('value').text
            except:
                pass

    # Recover data about Keywords (t) [Author Keywords, KeyWords Plus]
    def keywords(self, s, t):
        p = s.find_all('p', {'class': 'FR_field'})
        keywords = []
        for span_values in p:
            try:
                if(span_values.find('span').text == t):
                    v_values = span_values.find_all('a')
                    for k_value in v_values:
                        keywords = keywords + [k_value.text.upper()]
                    return ';'.join(keywords)
            except:
                pass

    # Extract data about Research Area
    def research_area(self, s):
        p = s.find_all('p', {'class': 'FR_field'})
        for si in p:
            try:
                if(si.find('span').text == 'Research Areas:'):
                    return si.get_text().replace('\n', '').replace('Research Areas:', '').replace(' - Other Topics', '').replace('; ', ';')
            except:
                pass

    def file_name(self, term):
        import re
        self.exp = '(TS=|TI=|AU=|AI=|GP=|ED=|SO=|DO=|PY=|CF=|AD=|OG=|OO=|SG=|SA=|CI=|PS=|CU=|ZP=|'
        self.exp = self.exp + 'FO=|FG=|FT=|SU=|WC=|IS=UT=|PMID|ALL=|AND |OR |\(|\)|\?|\:|\\|\/|\*|\<|\>|\||\")'
        return re.sub(self.exp, '', term).upper()

    def search(self, search_term):
        from requests import get
        from bs4 import BeautifulSoup
        import pandas as pd
        import re
        import time

        try:
            # Select only articles (need improve others selections)
            self.driver.find_element_by_xpath("//select/option[@value='Article']").click()
            time.sleep(2)

            self.elem.send_keys(search_term)
            self.driver.find_element_by_name("searchButton").click()

            # total de artigos encontrados
            self.total_paginas = self.driver.find_element_by_class_name("historyResults").text

            # Call results from history
            self.driver.find_element_by_class_name("historyResults").click()


            self.url = self.driver.current_url[:-1]
            self.url_base = self.url[:8] + self.url[8:].split('/')[0]
            self.article = {}
            self.article['link'] = []

            self.page = get(self.url + '1')

            soup = BeautifulSoup(self.page.content, 'html.parser')
            self.reference = soup.find(attrs={"class": "smallV110 snowplow-full-record"}).get('href')[:-1]
        except:

            self.driver.close()
            print("WARNING!\nNo articles were found for the search term.")

        try:
            for t_links in range(int(self.total_paginas.replace(",",""))):
                    #print(self.url_base + self.reference + str(t_links + 1))
                    self.article['link'].append(self.url_base + self.reference + str(t_links + 1))

            # Save tmp data to file
            df = pd.DataFrame(data=self.article)
            df.to_csv(self.file_name(search_term) + '_link.csv', index=False)

            # Cols to Dataset
            col_name = ['wos_id', 'doi', 'title', 'year', 'author', 'n_references', 'n_cited', 'journal', 'impact_factor', 'impact_factor_year', 'j_impact_factor_5_years', 'issn', 'eissn', 'author_keywords', 'keywords_plus', 'research_area', 'abstract']

            self.article = {name: [] for name in col_name}

            df = pd.read_csv(self.file_name(search_term) + '_link.csv')
            self.links = df.link.values

            # Array to keep errors
            self.v_errors = []

            # Verify the number of articles discovered
            tmp_warning = "\nWARNING!!!\n{} articles found.\nThe time to extract these articles can take considerably.\nIt is recommended to review the search term, because the WoS only show the first 10.000 results.\n\nDo you want to proceed with the extraction?\n".format(len(self.links))
            tmp_warning += "Type YES (upper case) to continue or ENTER to abort.\n\n"

            if len(self.links) > 200:
                confirm = input(tmp_warning)

                if confirm != 'YES':    
                    print("Operation canceled!")
                    self.driver.close()
                    sys.exit()

            print('\nFound {} links to scrap .... starting'.format(len(self.links)))

            # Confirm extraction if value is major at 200 articles
            if len(self.links) > 200:
                confirm = input(len(self.links), "articles found. Do you want to proceed with the extraction?")
                print('N or Y')

            for ii, link in enumerate(self.links, 1):
                try:
                    col = []
                    self.driver.get(link)

                    # seleciona o idioma inglês
                    self.driver.find_element_by_xpath('//html/body/div[1]/div[22]/ul[2]/li[3]').click()
                    self.driver.find_element_by_xpath('//html/body/div[1]/div[22]/ul[2]/li[3]/ul/li[3]/a').click()

                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    self.out = 'Scraping ' + str(ii).zfill(5) + ': ' + soup.find('div', {'class': 'title'}).text.replace('\n', '')
                    self.printer(self.out[0:50] + '...')

                    # WoS_id #
                    try:
                        col.append(self.wos_id(soup))
                    except:
                        col.append(0)

                    # DOI #
                    try:
                        col.append(self.doi(soup))
                    except:
                        col.append(0)

                    # Title of paper #
                    try:
                        col.append(soup.find('div', {'class': 'title'}).text.replace('\n', ''))
                    except:
                        col.append('No Title Available')

                    # Year of published #
                    try:
                        col.append(self.year_publised(soup))
                    except:
                        col.append('No year available')

                    # Authors #
                    try:
                        col.append(self.author_names(soup))
                    except:
                        col.append('No authors available')

                    # Number of references & Cited #
                    try:
                        ref, cited = self.number_ref_cited(soup)
                        col.append(ref)
                        col.append(cited)
                    except:
                        col.append(0)
                        col.append(0)

                    # Name of Journal #
                    try:
                        col.append(soup.find('p', {'class': 'sourceTitle'}).text.replace('\n', ''))
                    except:
                        col.append('No journal name available')

                    try:
                        # Impact factor current
                        col.append(self.impact_factor(soup)[0])
                    except:
                        col.append(0)

                    try:
                        # Impact factor year
                        col.append(self.impact_factor(soup)[1])
                    except:
                        col.append(0)

                    try:
                        # Impact factor five years
                        col.append(self.impact_factor(soup)[2])
                    except:
                        col.append(0)

                    # ISSN
                    try:
                        col.append(self.issn(soup))
                    except:
                        col.append(0)

                    # eISSN
                    try:
                        col.append(self.e_issn(soup))
                    except:
                        col.append(0)

                    # Author Keywords
                    try:
                        col.append(self.keywords(soup, 'Author Keywords:'))
                    except:
                        col.append('')

                    # Keywords Plus
                    try:
                        col.append(self.keywords(soup, 'KeyWords Plus:'))
                    except:
                        col.append('')

                    # Research Areas
                    try:
                        col.append(self.research_area(soup).upper())
                    except:
                        col.append('')

                    # Abstract
                    try:
                        col.append(self.abstract(soup))
                    except:
                        col.append('No abstract available')

                    for name, c in zip(col_name, col):
                        self.article[name].append(c)
                except:
                    self.v_errors = self.v_errors + [[self.wos_id(soup), soup.find('div', {'class': 'title'}).text.replace('\n', '')]]

            try:
                # Show & save in file errors if occurred #
                if( len(self.v_errors) > 0):
                    errors(self.v_errors, self.file_name(search_term))
            except:
                pass
            return pd.DataFrame(data=self.article)

        except:
            print('WARNING:\nThere were errors in the Web of Science request.\nTry again.')


