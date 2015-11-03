from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import glob
import os
from bs4 import BeautifulSoup


class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')


    def scripts_attr(self,tag, attrs):
        for s in self:
            if hasattr(s, 'name'):
                if s.name == "script":
                    continue
                for x in getStrings(s): yield x
            else:
                self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text


def main():
    dir_path = r"/home/maitreyee/Downloads/SchoolCollege.com/rajasthan_data/" #{origin dir path}
    results_dir = r"/home/maitreyee/Downloads/SchoolCollege.com/rajasthan_data/" #{dest dir path}
    for file_name in glob.glob(os.path.join(dir_path, "*.html")):
        f = open(file_name)
        text = f.read()
#            text = BeautifulSoup(html_file)
        results_file = os.path.splitext(file_name)[0] + '.txt'
#        print(dehtml(text))   
        with open(results_file, "w") as fp:
            fp.write(dehtml(text))
            fp.close()
#	print file_name
#        text = open(file_name)
#       results_file = os.path.splitext(file_name)[0] + '.txt'
#        with open(results_file, 'w') as outfile:
#            i = dehtml(text)
#    print(dehtml(text))
#            outfile.write(i + '\n')
#	    outfile.close()	


if __name__ == '__main__':
    main()

