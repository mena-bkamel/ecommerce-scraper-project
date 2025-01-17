class ProductFormat:
    def __init__(self, **kwargs):
        self.kw = kwargs

    def format_columns_definition(self) -> dict:
        """
        Formats column definitions based on provided data types.
        Converts input types into SQLite-compatible data types.
        """
        dic = {}
        for col_name, col_type in self.kw.items():
            col_type = col_type.lower()
            if col_type in ("null", "none"):
                dic[col_name] = "NULL"
            elif col_type in ("integer", "int", "boolean"):
                dic[col_name] = "INTEGER"
            elif col_type in ("float", "real"):
                dic[col_name] = "REAL"
            elif col_type in ("text", "str", "string"):
                dic[col_name] = "TEXT"
            elif col_type == "blob":
                dic[col_name] = "BLOB"
            else:
                raise ValueError(f"Unsupported data type for column '{col_name}': {col_type}")

        return dic
