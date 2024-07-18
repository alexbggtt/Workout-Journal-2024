import psycopg2
from config import config

class Operations:

    @staticmethod
    def connect():
        connection = None
        try:
            params = config()
            print('Connecting to PostgreSQL database')
            connection = psycopg2.connect(**params)

            # create a cursor
            cursor = connection.cursor()
            print('Database version')
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()  # Use fetchone() to fetch one row
            print(db_version)
            return cursor

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()
                print('Connection terminated')

    @staticmethod
    def data_adjustment(action, table, columns, values, where_columns=None, where_values=None):
        print('data_adjustment()')
        print(f'DEBUGGING CHECK\naction:{action}\ntable:{table}\ncolumns:{columns}\nvalues:{values}')
        try:
            connection = psycopg2.connect(**config())
            cursor = connection.cursor()

            # Perform the requested operation
            if action == 'INSERT':
                sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in range(len(columns))])})"
                cursor.execute(sql, values)
            elif action == 'UPDATE':
                set_clause = ', '.join([f"{col} = %s" for col in columns])
                where_clause = ' AND '.join([f"{col} = %s" for col in where_columns]) if where_columns else ''
                sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"

                # Format the workout_vector array correctly
                formatted_values = []
                for value in values:
                    if isinstance(value, list):
                        if isinstance(value[0], list):
                            formatted_value = '{' + ','.join(
                                ['{' + ','.join(map(str, subarray)) + '}' for subarray in value]) + '}'
                        else:
                            formatted_value = '{' + ','.join(map(str, value)) + '}'
                        formatted_values.append(formatted_value)
                    else:
                        formatted_values.append(value)

                # Convert the formatted values to a tuple
                formatted_values = tuple(formatted_values)

                print(f'SQL Query: {sql}')
                print(f'Formatted Values: {formatted_values}')
                cursor.execute(sql, formatted_values + tuple(where_values if where_values else []))
            elif action == 'DELETE':
                where_clause = ' AND '.join([f"{col} = %s" for col in where_columns])
                sql = f"DELETE FROM {table} WHERE {where_clause}"
                cursor.execute(sql, where_values)
            else:
                print(f"Invalid action: {action}")
                return

            # Commit the changes and close the connection
            connection.commit()
            print(f"{action} operation performed successfully.")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error performing {action} operation: {error}")
            connection.rollback()
        finally:
            if connection is not None:
                connection.close()


    @staticmethod
    def get_tables():
        try:
            # Connect to the database
            params = config()
            connection = psycopg2.connect(**params)
            cursor = connection.cursor()

            # Execute the query to get all tables
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'")

            # Fetch all rows
            tables = cursor.fetchall()

            # Print the tables
            print("Tables in the database:")
            for table in tables:
                print(table[0])  # Table name is in the first column

            # Close cursor and connection
            cursor.close()
            connection.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error:", error)

    @staticmethod
    def data_retrieval(table, columns, where_columns=None, where_values=None, order_by=None):
        print(f'dtaretrival(): table: {table}\ncolumn: {columns}')
        try:
            connection = psycopg2.connect(**config())
            cursor = connection.cursor()

            select_columns = ', '.join(columns)
            sql = f"SELECT {select_columns} FROM {table}"

            if where_columns and where_values:
                where_clause = ' AND '.join([f"{col} = %s" for col in where_columns])
                sql += f" WHERE {where_clause}"

            if order_by:
                sql += f" ORDER BY {order_by}"

            if where_columns and where_values:
                cursor.execute(sql, where_values)
            else:
                cursor.execute(sql)

            results = cursor.fetchall()
            connection.close()
            return results

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error retrieving data: {error}")
            return []