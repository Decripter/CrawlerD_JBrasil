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
    pricce_month = Item("pricce_month")

    content = ""
    content_list = []

    def __init__(self, url, delimiter_start, delimiter_end, cut_slice_pattern):

        req = urllib.request.Request(url)

        req.add_header("User-Agent", "urllib-example/0.1 (Contact: . . .)")
        content = str(urllib.request.urlopen(req).read())

        posicao_start = int(content.index(delimiter_start))
        posicao_end = int(content.index(delimiter_end))

        extracted_content = content[posicao_start:posicao_end]

        content_whitout_n = extracted_content.replace("\\n", "")
        content = content_whitout_n.replace("\\t", "")

        self.content = content.split(cut_slice_pattern)

    def find_item_content(self, row_content, item):

        position_s = int(row_content.index(item.find_pattern_start))
        position_e = int(row_content.index(item.find_pattern_end))

        result = row_content[
            position_s + len(item.find_pattern_start) : position_e + item.leters_to_add
        ]
        content = result.replace(item.to_remove, "")
        return content

    def extract_content(self):
        for row in self.content:
            cpu = self.find_item_content(row, self.cpu)
            memory = self.find_item_content(row, self.memory)
            storage = self.find_item_content(row, self.storage)
            bandwidth = self.find_item_content(row, self.bandwidth)
            price_month = self.find_item_content(row, self.pricce_month)

            self.content_list.append(
                {
                    "cpu": cpu,
                    "memory": memory,
                    "storage": storage,
                    "bandwidth": bandwidth,
                    "price_month": price_month,
                }
            )