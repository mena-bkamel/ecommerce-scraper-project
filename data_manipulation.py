import pandas as pd


class DataManipulation:

    def merge_files(self, files: tuple | list):
        files_read = [pd.read_csv(file) for file in files]
        merged = pd.concat(files_read, ignore_index=True)
        return merged

    def create_csv_file(self, dataframe, file_name):

        if isinstance(dataframe, pd.DataFrame):
            if not file_name.endswith(".csv"):
                file_name += ".csv"

            dataframe.to_csv(file_name, index=False)
        else:
            print("Error: Input must be Pandas Dataframe.")


if __name__ == '__main__':
    dm = DataManipulation()
    mer = dm.merge_files(["a.csv", "b.csv"])

    dm.create_csv_file(mer, "amazon_file.csv")
