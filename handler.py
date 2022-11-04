from sys import argv
import ClassFileHandler


def get_permission() -> bool:
    """Checking for permission to display information / delete files."""
    while True:
        check = input()
        if check == "yes":
            return True
        elif check == "no":
            return False
        else:
            print("Wrong option")


def main():
    if len(argv) < 2:
        print("Directory is not specified")
        exit(1)

    file_handler = ClassFileHandler.FileHandler(argv[1])
    print(file_handler)

    print("\nCheck for duplicates?")
    if get_permission():
        file_handler.print_duplicates()

        print("\nDelete files?")
        if get_permission():
            file_handler.remove_duplicates()


if __name__ == "__main__":
    main()
