import csv
import time
import structlog

from io import StringIO

from src.settings import settings


logger = structlog.get_logger('__name__')


def psql_insert_copy(table, conn, keys, data_iter):
    connection = conn.connection
    with connection.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


def load_data(data):
    engine = settings.DATABASE_ENGINE

    start_time = time.time()
    data.to_sql(
        name='test',
        con=engine,
        if_exists='append',
        index=False,
        method=psql_insert_copy
    )
    end_time = time.time()
    logger.info(f'Insert time: {end_time - start_time} seconds')
