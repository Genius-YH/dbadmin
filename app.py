from flask import flash, redirect, render_template, request, url_for, Response
from sqlalchemy import Table, select, insert
from sqlalchemy.exc import SQLAlchemyError

from dbadmin.domain.validators import quote_ident
from dbadmin.interfaces.web.factory import build_container

app, gateways, services = build_container()


def get_ctx():
    conn_name = request.args.get("conn") or request.form.get("conn") or "default"
    if conn_name not in gateways:
        conn_name = "default"
    return conn_name, gateways[conn_name], services[conn_name]


@app.get("/")
def index():
    conn_name, _, service = get_ctx()
    schemas = service.list_schemas()
    current_schema = request.args.get("schema") or (schemas[0] if schemas else "")
    table_rows = service.list_tables(current_schema) if current_schema else []
    return render_template("index.html", conn_name=conn_name, connections=sorted(gateways.keys()), schemas=schemas, current_schema=current_schema, table_rows=table_rows)


@app.post("/schema/create")
def schema_create():
    conn_name, _, service = get_ctx()
    schema = request.form.get("schema", "")
    try:
        service.create_schema(schema)
        flash("스키마가 생성되었습니다.", "success")
    except (SQLAlchemyError, ValueError) as exc:
        flash(f"스키마 생성 실패: {exc}", "error")
    return redirect(url_for("index", conn=conn_name, schema=schema))


@app.get('/table/<schema>/<table_name>')
def table_view(schema: str, table_name: str):
    conn_name, gateway, _ = get_ctx()
    table: Table = gateway.metadata(schema).tables[f"{schema}.{table_name}"]
    with gateway.engine.connect() as conn:
        rows = conn.execute(select(table).limit(app.config["MAX_ROWS"])).mappings().all()
    return render_template("table.html", conn_name=conn_name, schema=schema, table_name=table_name, columns=[c.name for c in table.columns], pk_cols=[c.name for c in table.primary_key.columns], rows=rows)


@app.post('/table/<schema>/<table_name>/insert')
def table_insert(schema: str, table_name: str):
    conn_name, gateway, _ = get_ctx()
    table: Table = gateway.metadata(schema).tables[f"{schema}.{table_name}"]
    payload = {c.name: request.form.get(c.name) for c in table.columns if request.form.get(c.name, "") != ""}
    try:
        with gateway.engine.begin() as conn:
            conn.execute(insert(table).values(**payload))
    except SQLAlchemyError as exc:
        flash(f"삽입 실패: {exc}", "error")
    return redirect(url_for('table_view', conn=conn_name, schema=schema, table_name=table_name))


@app.get('/admin/export/schema/<schema>')
def export_schema(schema: str):
    conn_name, gateway, _ = get_ctx()
    tables = gateway.execute("SELECT table_name FROM information_schema.tables WHERE table_schema=:schema ORDER BY table_name", {'schema': schema}).all()
    lines = [f"-- schema: {schema}", f"CREATE DATABASE IF NOT EXISTS {quote_ident(schema)};", f"USE {quote_ident(schema)};"]
    for (table_name,) in tables:
        create_row = gateway.execute(f"SHOW CREATE TABLE {quote_ident(schema)}.{quote_ident(table_name)}").first()
        if create_row:
            lines.append(create_row[1] + ";")
    return Response("\n\n".join(lines)+"\n", mimetype="text/sql", headers={"Content-Disposition": f"attachment; filename={conn_name}_{schema}.sql"})


if __name__ == '__main__':
    app.run(debug=True)
