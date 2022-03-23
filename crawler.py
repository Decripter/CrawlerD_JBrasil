import time
import random
import urllib.request


class Item:

    name = ""
    find_pattern_start = ""
    find_pattern_end = ""
    to_remove = ""
    leters_to_add = 0

    def __init__(self, name):
        self.name = name


class Crawler:

    cpu = Item("cpu")
    memory = Item("memory")
    storage = Item("storage")
    bandwidth = Item("bandwidth")
    price_month = Item("price_month")

    url_root = ""  # this is extracted from url like http://abc.com/teste/alfa => http://abc.com

    content = ""  # this will contain the raw data feched
    content_list = []  # this will contain the clean and structured data

    def __init__(self, url, delimiter_start, delimiter_end, cut_slice_pattern):

        self.url_root = self.get_url_root(url)

        req = urllib.request.Request(url)

        req.add_header("User-Agent", "urllib-example/0.1 (Contact: . . .)")
        content = str(urllib.request.urlopen(req).read())

        try:  # try fetch the tata from url
            position_start = int(content.index(delimiter_start))
            position_end = int(content.index(delimiter_end))

        except ValueError:  # if dont find the data, look to links on the page to find the path

            links = self.find_links(content)  # extract the urls

            for link in links:  # try into each link

                if link.find(".") != -1:
                    print( "Url ignored: " + self.url_root + "" + link )  # ignore links that contains '.' like aas.css or abc.com
                    continue

                print("Trying fetch data from: " + self.url_root + "" + link)
                time.sleep( random.randint(1, 4))  # wait 1-4 seconds between each try to avoid firewall block

                try:  # try fetch again using links

                    req = urllib.request.Request( self.url_root + "" + link )  # url root + link extracted
                    req.add_header("User-Agent", "urllib-example/0.1 (Contact: . . .)")
                    content = str(urllib.request.urlopen(req).read())

                    position_start = int(content.index(delimiter_start))
                    position_end = int(content.index(delimiter_end))

                except urllib.error.URLError:  # invalid url

                    continue

                except ValueError:  # data dont find

                    continue

                else:

                    extracted_content = content[position_start:position_end]

                    content_whitout_n = extracted_content.replace("\\n", "")
                    content = content_whitout_n.replace("\\t", "")

                    self.content = content.split(cut_slice_pattern)

                    break  # stop loop for
        else:

            extracted_content = content[ position_start:position_end ]  # extract the data between delimiters

            content_whitout_n = extracted_content.replace( "\\n", "" )  # the raw data contains specials characters
            content = content_whitout_n.replace("\\t", "")

            self.content = content.split( cut_slice_pattern )  # create a list of rows from the raw data

    def extract_item_content(self, row_content, item):

        position_s = int(row_content.index(item.find_pattern_start))
        position_e = int(row_content.index(item.find_pattern_end))

        result = row_content[ position_s + len(item.find_pattern_start) : position_e + item.leters_to_add ]

        content = result.replace(item.to_remove, "")

        return content

    def extract_full_content(self):
        for row in self.content:
            cpu = self.extract_item_content(row, self.cpu)
            memory = self.extract_item_content(row, self.memory)
            storage = self.extract_item_content(row, self.storage)
            bandwidth = self.extract_item_content(row, self.bandwidth)
            price_month = self.extract_item_content(row, self.price_month)

            self.content_list.append(
                {
                    "cpu": cpu,
                    "memory": memory,
                    "storage": storage,
                    "bandwidth": bandwidth,
                    "price_month": price_month,
                }
            )

    def get_url_root(self, url):

        url_root = ""

        for char in range(len(url) - 1):

            if (
                url[char] == "/"
                and url[char + 1] != "/"
                and url[char] == "/"
                and url[char - 1] != "/"
            ):
                url_root = url[:char]

                break

        return url_root

    def find_links(self, content):

        links = []
        result_end = []

        # find links based on the 'href' atribute it return a list of position where start each link
        result = [i for i in range(len(content)) if content.startswith("href=", i)] 

        for href in result:
            # search for the end of href atribuute looking for the close (")
            result_end.append(content[href + 6 :].find('"'))

        for link in range(len(result)):
            # fill thenlinks array with extracted links from result position to result_end position
            links.append( content[result[link] + 6 : result[link] + result_end[link] + 6] )

        return links
