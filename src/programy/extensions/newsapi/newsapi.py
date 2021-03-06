"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.utils.newsapi.newsapi import NewsAPI

class NewsAPIExtension(object):

    def get_news_api_api(self, bot, clientid):
        return  NewsAPI(bot.license_keys)

    def get_news(self, bot, clientid, source, max, sort, reverse):

        newsapi = self.get_news_api_api(bot, clientid)

        headlines = newsapi.get_headlines(source, max, sort, reverse)
        if headlines is None:
            logging.error("NewsAPIExtension no headlines found!")
            return ""

        results = newsapi.to_program_y_text(headlines)
        if results is None:
            logging.error("NewsAPIExtension no results returned!")
            return ""

        return results

    def parse_data(self, data):
        source = None
        max = 10
        sort = False
        reverse = False

        splits = data.split()
        count = 0
        while count < len(splits):
            if splits[count] == "SOURCE":
                count += 1
                source = splits[count]
            elif splits[count] == "MAX":
                count += 1
                max = int(splits[count])
            elif splits[count] == "SORT":
                count += 1
                if splits[count].upper() == 'TRUE':
                    sort = True
                elif splits[count].upper() == 'FALSE':
                    sort = False
                else:
                    logging.error("Invalid value for NewAPI Data parameter sort [%s]"%splits[count])
                    sort = False
            elif splits[count] == "REVERSE":
                count += 1
                if splits[count].upper() == 'TRUE':
                    reverse = True
                elif splits[count].upper() == 'FALSE':
                    reverse = False
                else:
                    logging.error("Invalid value for NewAPI Data parameter reverse [%s]"%splits[count])
                    reverse = False
            count += 1

        return source, max, sort, reverse

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, bot, clientid, data):

        source, max, sort, reverse = self.parse_data(data)

        if source is None:
            logging.error("NewsAPIExtension no source passed in as data parameter!")
            return ""

        return self.get_news(bot, clientid, source, max, sort, reverse)

