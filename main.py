import sys  # for handling arguments
from crawler import Crawler


def get_vultr():
    vultr = Crawler(
        "https://www.vultr.com/pricing/#cloud-compute/",
        "<!-- CLOUD COMPUTE -->",
        "<!-- DEDICATED CLOUD COMPUTE -->",
        "pt__row-content",
    )  # Instance of Crawler_object

    vultr.cpu.find_pattern_start = 'data-row=""><div class="pt__cell js-price"><strong>'
    vultr.cpu.find_pattern_end = 'CPU</div><div class="pt_'
    vultr.cpu.to_remove = "</strong>&nbsp;"
    vultr.cpu.leters_to_add = 3

    vultr.memory.find_pattern_start = 'PU</div><div class="pt__cell js-price"><strong>'
    vultr.memory.find_pattern_end = "</strong>&nbsp;GB"
    vultr.memory.to_remove = "</strong>&nbsp;"
    vultr.memory.leters_to_add = len(vultr.memory.find_pattern_end)

    vultr.storage.find_pattern_start = (
        'dth</span></div><div class="pt__cell js-price"><strong>'
    )
    vultr.storage.find_pattern_end = 'GB<span class="is-hidden-lg-up"> Storage'
    vultr.storage.to_remove = "</strong>&nbsp;"
    vultr.storage.leters_to_add = 2

    vultr.bandwidth.find_pattern_start = (
        'Memory</span></div><div class="pt__cell js-price"><strong>'
    )
    vultr.bandwidth.find_pattern_end = 'TB<span class="is-hidden-lg-up"> Bandwidth'
    vultr.bandwidth.to_remove = "</strong>&nbsp;"
    vultr.bandwidth.leters_to_add = len(vultr.bandwidth.find_pattern_end)

    vultr.pricce_month.find_pattern_start = 'pt__cell--price pt__cell-price"><strong>'
    vultr.pricce_month.find_pattern_end = " </strong>&nbsp;/mo</div>"

    vultr.content.pop(0)  # discard the header
    vultr.extract_full_content()

    return vultr.content_list


def print_list_arguments_help():
    print(  # print help
        """
--print url => Print results directly on screen
--save_csv url => Store results on csv file
--save_json url => Store results on json format file

If any url is passed as argument the default_urls.txt files will be used as argument.
    """
    )


def print_error_lack_arguments(args_passed):
    if len(args_passed) == 1:
        print("You dont pass any argument, this is a help:")
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

    elif sys.argv[1] == "--save_csv":
        pass
    elif sys.argv[1] == "--save_json":
        pass
