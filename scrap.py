"""
Module to read through the Udacity Bertelsmann Scholarship to fetch the names
of the participants from the web page.
"""


from bs4 import BeautifulSoup  # pip3 install beautifulsoup4
import urllib3                 # pip3 install urllib3


class Scrap:
    """Main class with methods to read and parse the web page.
    """

    def __init__(self):
        """This is a constructor, initialises a pool for making HTTP request
        and also initialises a variable with the url to the wall page.
        """

        self.http = urllib3.PoolManager()
        self.data_track_url = 'https://sites.google.com/udacity.com/bertelsmann-challenge' \
                              '/data-track/data-honorable-mentions-wall'

    def get_web_page(self):
        """This method request the web-page and fetches the response from the
        web-page and return the response in a variable.
        """

        # client = urlopen(my_url)
        response = self.http.request(method='GET', url=self.data_track_url)

        # offload the content into a variable
        page_html = response.data

        # close the connection
        response.close()

        return page_html

    def parse_web_page(self, page_html):
        """
        This method parses the response we stored in page_html
        and read all the <p> paragraphs in the html web-page
        and put all the strings (from paragraphs) into a variable
        paragraphs and returns it.

        :param page_html: (str) contains the response from the web-page.
        :return paragraph: (str) contains all the strings from the <p>
        tags on the html page.
        """

        # Beautifulsoup is a html parser there are several
        # other available in the market.
        page_soup = BeautifulSoup(page_html, "html.parser")

        # read all the paragraphs in the web page
        paragraphs = page_soup.findAll('p')

        return paragraphs

    def read_web_page(self, paragraphs):
        """
        This method reads the paragraph variables and put the strings in
        between the <p></p> tag into a list called 'names', and then we remove
        the garbage strings using the names.remove
        """

        names = []

        # list of words that we check in the string <p></p>
        # and if found we remove them from the names[] list.
        omission_list = ['student', 'completes', 'complete',
                         'completion', 'Completion']

        # collected all string between <p> </p> below in a list.
        for para in paragraphs:
            names.append(para.getText())

        # removed all the list items that has string matching from omission list.
        for omit in omission_list:
            for name in names:
                if omit in name:
                    names.remove(name)

        print('Unique names on the wall:')
        print(sorted(set(names)))  # remove all the duplicate entries and print list
        print(f'There are total {len(set(names))} unique names on the wall.')

    def main(self):
        """Main method of the class that calls all other methods
        of the Modules and manages the flow of the module.
        """

        page_html = self.get_web_page()
        para = self.parse_web_page(page_html=page_html)
        self.read_web_page(paragraphs=para)


if __name__ == '__main__':
    scrap = Scrap()
    scrap.main()
