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

    url_root = ""

    content = ""
    content_list = []

    def __init__(self, url, delimiter_start, delimiter_end, cut_slice_pattern):

        self.url_root = self.get_url_root(url)

        req = urllib.request.Request(url)

        req.add_header("User-Agent", "urllib-example/0.1 (Contact: . . .)")
        content = str(urllib.request.urlopen(req).read())
        try:
            position_start = int(content.index(delimiter_start))
            position_end = int(content.index(delimiter_end))

        except ValueError:

            links = self.find_links(content)

            for link in links:

                if link.find(".") != -1:
                    print("Url ignored: " + self.url_root + "" + link)
                    continue
                print("Trying fetch data from: " + self.url_root + "" + link)
                time.sleep(random.randint(1, 4))

                try:

                    req = urllib.request.Request(self.url_root + "" + link)
                    req.add_header("User-Agent", "urllib-example/0.1 (Contact: . . .)")
                    content = str(urllib.request.urlopen(req).read())

                    position_start = int(content.index(delimiter_start))
                    position_end = int(content.index(delimiter_end))

                except urllib.error.URLError:

                    continue

                except ValueError:

                    continue

                else:

                    extracted_content = content[position_start:position_end]

                    content_whitout_n = extracted_content.replace("\\n", "")
                    content = content_whitout_n.replace("\\t", "")

                    self.content = content.split(cut_slice_pattern)
                    break
        else:

            extracted_content = content[position_start:position_end]

            content_whitout_n = extracted_content.replace("\\n", "")
            content = content_whitout_n.replace("\\t", "")

            self.content = content.split(cut_slice_pattern)

    def extract_item_content(self, row_content, item):

        position_s = int(row_content.index(item.find_pattern_start))
        position_e = int(row_content.index(item.find_pattern_end))

        result = row_content[
            position_s + len(item.find_pattern_start) : position_e + item.leters_to_add
        ]

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

        result = [i for i in range(len(content)) if content.startswith("href=", i)]

        for href in result:

            result_end.append(content[href + 6 :].find('"'))

        for link in range(len(result)):

            links.append(
                content[result[link] + 6 : result[link] + result_end[link] + 6]
            )

        return links
