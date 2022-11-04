import hashlib
import os


class FileHandler:
    DESCENDING, ASCENDING = 1, 2

    def __init__(self, root_folder):
        self.root_folder = root_folder
        self.file_format = self.choosing_file_format()
        self.all_paths = list(self.get_all_paths())
        self.files_size = self.get_files_same_size()
        self.duplicates = self.get_duplicates()

    @staticmethod
    def choosing_file_format() -> str:
        print("\nEnter file format:")
        return input()

    def choosing_sorting_options(self) -> int:
        print("\nSize sorting options:",
              "1. Descending",
              "2. Ascending", sep="\n")
        while True:
            try:
                print("\nEnter a sorting option:")
                sorting = int(input())
                if sorting not in [self.DESCENDING, self.ASCENDING]:
                    raise ValueError
                else:
                    return sorting
            except ValueError:
                print("\nWrong option")

    def get_all_paths(self) -> str:
        """Get all the paths to files located in a given directory."""
        for root, dirs, files in os.walk(self.root_folder, topdown=True):
            for name in files:
                if self.file_format in name:
                    yield os.path.join(root, name)

    def get_files_same_size(self) -> dict:
        """Generates a dictionary whose keys are the file sizes, and the values are all the paths to these files."""
        intermediate_dict = {}
        for path in self.all_paths:
            key = os.path.getsize(path)
            intermediate_dict = self.filling_intermediate_dictionary(intermediate_dict, key, path)

        files_size = self.get_dictionary_necessary(intermediate_dict)
        return self.get_sorted_dict(files_size)

    def get_sorted_dict(self, files_size) -> dict:
        """Selects the type of sorting (descending or ascending) and returns it."""
        sorting = self.choosing_sorting_options()
        reverse = True if sorting == self.DESCENDING else False
        sorted_files_size = {k: v for k, v in sorted(files_size.items(), reverse=reverse)}

        return sorted_files_size

    def get_duplicates(self) -> dict:
        """Gets a hash dictionary with the value of duplicate file paths."""
        intermediate_dict = {}
        for values in self.files_size.values():
            for path in values:
                with open(path, "rb") as first_file:
                    key = hashlib.md5(first_file.read()).hexdigest()

                intermediate_dict = self.filling_intermediate_dictionary(intermediate_dict, key, path)

        duplicates = self.get_dictionary_necessary(intermediate_dict)
        return duplicates

    @classmethod
    def get_dictionary_necessary(cls, intermediate_dict) -> dict:
        """Get a dictionary from a shared dictionary that contains more than one file path"""
        necessary_dictionary = {}
        for key, paths in intermediate_dict.items():
            if len(paths) > 1:
                necessary_dictionary[key] = paths
        return necessary_dictionary

    @classmethod
    def filling_intermediate_dictionary(cls, intermediate_dict, key, path) -> dict:
        """Filling in the intermediate dictionary"""
        if intermediate_dict.get(key) is None:
            intermediate_dict[key] = [path]
        else:
            intermediate_dict[key].append(path)
        return intermediate_dict

    def __str__(self) -> str:
        """Prints the file size and paths with the same size."""
        str_ = ""
        for key, values in self.files_size.items():
            str_ += f"\n{key} bytes\n"
            str_ += "\n".join(values) + "\n"
        return str_[:-1]

    def print_duplicates(self) -> None:
        """Prints the duplicate dictionary and its size."""
        hash_pats = str_ = ""
        counter = 1

        for size_key, all_paths in self.files_size.items():
            size_str = f"\n{size_key} bytes\n"
            for hash_key, paths in self.duplicates.items():
                if paths[0] in all_paths:
                    hash_pats += f"Hash: {hash_key}\n"
                    for path in paths:
                        hash_pats += f"{counter}. {path}\n"
                        counter += 1

            if hash_pats != "":
                str_ += size_str + hash_pats
                hash_pats = ""

        print(str_[:-1])

    def remove_duplicates(self) -> None:
        """Deleting duplicates by their number and displaying the total size of deleted files in bytes."""
        lst_remove = self.checking_duplicate_number()
        paths = [path for paths in self.duplicates.values() for path in paths]
        total_free_space = 0

        for index, path in enumerate(paths):
            if index + 1 in lst_remove:
                for key, values in self.files_size.items():
                    if path in values:
                        total_free_space += key
                        os.remove(path)

        print(f"Total freed up space: {total_free_space} bytes")

    def checking_duplicate_number(self) -> list:
        """Checking for the correct entry of the sequence numbers of duplicate files for deletion."""
        print("\nEnter file numbers to delete:\n")
        while True:
            try:
                lst_number = list(map(int, input().split()))
                duplicate_numbers = sum(len(x) for x in self.duplicates.values())

                if lst_number:
                    for i in lst_number:
                        if not 0 < i <= duplicate_numbers:
                            raise ValueError
                    return lst_number
                raise ValueError

            except ValueError:
                print("Wrong format")