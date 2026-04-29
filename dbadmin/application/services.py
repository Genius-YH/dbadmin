from dbadmin.domain.validators import quote_ident, quote_string, is_valid_ident, is_valid_host


class AdminService:
    def __init__(self, gateway):
        self.gw = gateway

    def list_schemas(self):
        return [r[0] for r in self.gw.execute("SHOW DATABASES").all()]

    def list_tables(self, schema: str):
        return self.gw.execute(
            "SELECT table_name, table_rows, engine, create_time, update_time FROM information_schema.tables WHERE table_schema=:schema ORDER BY table_name",
            {"schema": schema},
        ).mappings().all()

    def create_schema(self, schema: str):
        self.gw.execute_tx(f"CREATE DATABASE {quote_ident(schema)}")

    def drop_schema(self, schema: str):
        self.gw.execute_tx(f"DROP DATABASE {quote_ident(schema)}")

    def create_user(self, user: str, host: str, password: str):
        if not is_valid_ident(user) or not is_valid_host(host):
            raise ValueError("invalid user/host")
        self.gw.execute_tx(f"CREATE USER {quote_string(user)}@{quote_string(host)} IDENTIFIED BY {quote_string(password)}")
