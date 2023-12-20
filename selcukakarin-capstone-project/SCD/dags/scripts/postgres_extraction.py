import  psycopg2

def exec_postgres_extraction():
    """
    Connect to postgres and write data from product_content table to csv file
    """
    # Create an extract query
    query = "SELECT * FROM bootcamp.public.product_content"
    sql = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    # Define destination csv path
    file_path = "/usr/local/airflow/dags/datas/product_content_data.csv"

    t_host = "34.107.1.19" # Either a domain name, an IP address, or "localhost"
    t_port = "5432" # This is the default postgres port
    t_dbname = "bootcamp"
    t_user = "bootcamp"
    t_pw = "bootcamp2021!"

    # Make a connection to postgres with psycopg2
    conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
    cur = conn.cursor()

    try:
        # Execute extraction query
        with open(file_path, 'w', encoding='utf-8') as file:
            cur.copy_expert(sql, file)
    except psycopg2.Error as e:
        t_message ="Error"
        print(t_message)
    finally:
        cur.close()

if __name__ == "__main__":
    # Extract postgres datas to csv file
    exec_postgres_extraction()