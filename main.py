import json
import csv
import sys  # for handling arguments
from crawler import Crawler


def get_vultr():

    # Instance of Crawler_object 

    vultr = Crawler(
        "https://www.vultr.com/products/cloud-compute/#pricing",
        "<!-- CLOUD COMPUTE -->",
        "<!-- DEDICATED CLOUD COMPUTE -->",
        "pt__row-content",
    )

    # Pattern to find CPU data
    vultr.cpu.find_pattern_start = 'data-row=""><div class="pt__cell js-price"><strong>'
    vultr.cpu.find_pattern_end = 'CPU</div><div class="pt_'
    vultr.cpu.to_remove = "</strong>&nbsp;"
    vultr.cpu.leters_to_add = 3

    # Pattern to find Memory data
    vultr.memory.find_pattern_start = 'PU</div><div class="pt__cell js-price"><strong>'
    vultr.memory.find_pattern_end = "</strong>&nbsp;GB"
    vultr.memory.to_remove = "</strong>&nbsp;"
    vultr.memory.leters_to_add = len(vultr.memory.find_pattern_end)

    # Pattern to find Storage data
    vultr.storage.find_pattern_start = (
        'dth</span></div><div class="pt__cell js-price"><strong>'
    )
    vultr.storage.find_pattern_end = 'GB<span class="is-hidden-lg-up"> Storage'
    vultr.storage.to_remove = "</strong>&nbsp;"
    vultr.storage.leters_to_add = 2

    # Pattern to find Bandwidth data
    vultr.bandwidth.find_pattern_start = (
        'Memory</span></div><div class="pt__cell js-price"><strong>'
    )
    vultr.bandwidth.find_pattern_end = 'TB<span class="is-hidden-lg-up"> Bandwidth'
    vultr.bandwidth.to_remove = "</strong>&nbsp;"
    vultr.bandwidth.leters_to_add = 2

    # Pattern to find Price/Month data
    vultr.price_month.find_pattern_start = 'pt__cell--price pt__cell-price"><strong>'
    vultr.price_month.find_pattern_end = " </strong>&nbsp;/mo</div>"

    vultr.content.pop(0)  # discard the header
    vultr.extract_full_content()

    return vultr.content_list

def export_json(dictionary, name):
    with open(name+'.json', "w") as outfile:
        json.dump(dictionary, outfile)

def export_csv(to_csv, name):

    keys = to_csv[0].keys()

    with open(name+'.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(to_csv)

def print_list_arguments_help():
    print(  # print help
        """
--print Crawler_object => Print results directly on screen
--save_csv Crawler_object => Store results on csv file
--save_json Crawler_object => Store results on json format file

If any url is passed as argument the default_urls.txt files will be used as argument.
    """
    )


def print_error_lack_arguments(args_passed):
    if len(args_passed) == 1:
        print("You don't pass any argument, this is a help:")
        print_list_arguments_help()


if len(sys.argv) < 2:
    print_error_lack_arguments(sys.argv)
else:
    if sys.argv[1] == "--print":
        if len(sys.argv) > 2:
            if sys.argv[2] == "vultr":
                print(get_vultr())
        else:
            print("You must be pass more one argument => Crawler_object")

    elif sys.argv[1] == "--save_json":
        if len(sys.argv) > 2:
            if sys.argv[2] == "vultr":
                export_json(get_vultr(), "vultr")
        else:
            print("You must be pass more one argument => Crawler_object")

    elif sys.argv[1] == "--save_csv":
        if len(sys.argv) > 2:
            if sys.argv[2] == "vultr":
                export_csv(get_vultr(), "vultr")
        else:
            print("You must be pass more one argument => Crawler_object")

    else:
        print("You pass an invalid argument, this is a help:")
        print_list_arguments_help()