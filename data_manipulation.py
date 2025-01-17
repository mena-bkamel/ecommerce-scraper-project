import pandas as pd


class DataManipulation:
    def merge_files(self, files: tuple | list, new_file_name):
        files_read = [pd.read_csv(file) for file in files]
        merged = pd.concat(files_read, ignore_index=True)
        merged.to_csv(f"{new_file_name}.csv", index=False)
        print("CSV files merged successfully!")




