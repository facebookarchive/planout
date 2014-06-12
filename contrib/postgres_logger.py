from planout.experiment import SimpleExperiment

import psycopg2 as pg
from psycopg2.extras import Json as pJson

class PostgresLoggedExperiment(SimpleExperiment):

    def configure_logger(self):
        """ Sets up a logger to postgres.

        1. Modify the connection_parameters variable to be a dictionary of the
        parameters to create a connection to your postgres database.
        2. Modify the table variable to be the table to which you plan on
        logging.
        """

        connection_parameters = {'host': 'localhost',
                                 'database': 'experiments'}
        table = 'experiments'

        self.conn = pg.connect(**connection_parameters)
        self.table = table

    def log(self, data):
        """ Log exposure. """

        columns = ['inputs', 'name', 'checksum', 'params', 'time', 'salt',
                   'event']

        names = ','.join(columns)
        placeholders = ','.join(['%s']*len(columns))
        ins_statement = ('insert into {} ({}) values ({})'
                         .format(self.table, names, placeholders))

        row = []
        for column in columns:
            value = data[column]
            row.append(pJson(value) if isinstance(value, dict) else value)

        with self.conn.cursor() as curr:
            curr.execute(ins_statement, row)

        self.conn.commit()
