class ProductFormat:
    def __init__(self, **kwargs):
        self.kw = kwargs
        self.header_row = []
        self.col_definition_db = {}

    def format_columns(self):
        """
        Formats column definitions based on provided data types.
        Converts input types into SQLite-compatible data types.
        """
        for col_name, col_type in self.kw.items():
            self.header_row.append(col_name)

            col_type = col_type.lower()
            if col_type in ("null", "none"):
                self.col_definition_db[col_name] = "NULL"
            elif col_type in ("integer", "int", "boolean"):
                self.col_definition_db[col_name] = "INTEGER"
            elif col_type in ("float", "real"):
                self.col_definition_db[col_name] = "REAL"
            elif col_type in ("text", "str", "string"):
                self.col_definition_db[col_name] = "TEXT"
            elif col_type == "blob":
                self.col_definition_db[col_name] = "BLOB"
            else:
                raise ValueError(f"Unsupported data type for column '{col_name}': {col_type}")

