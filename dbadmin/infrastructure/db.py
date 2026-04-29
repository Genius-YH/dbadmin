from sqlalchemy import create_engine, text, MetaData


class SqlAlchemyGateway:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)

    def execute(self, sql: str, params: dict | None = None):
        with self.engine.connect() as conn:
            return conn.execute(text(sql), params or {})

    def execute_tx(self, sql: str, params: dict | None = None):
        with self.engine.begin() as conn:
            return conn.execute(text(sql), params or {})

    def metadata(self, schema: str | None = None):
        md = MetaData(schema=schema)
        md.reflect(bind=self.engine, schema=schema)
        return md
