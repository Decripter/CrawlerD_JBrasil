import sys  # for handling arguments


def print_list_arguments_help():
    print(
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
        print("you must print", sys.argv[2])
    elif sys.argv[1] == "--save_csv":
        pass
    elif sys.argv[1] == "--save_json":
        pass
