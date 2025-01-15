import csv


class DataSaving:
    def __init__(self):
        ...

    def save_to_csv(self, file_name: str, header: list, records: list[tuple], mode="w"):
        file_name = file_name.replace(" ", "_").lower()
        with open(f"{file_name}.csv", mode, newline='', encoding='utf-8') as f:
            if mode == "w":
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(records)

