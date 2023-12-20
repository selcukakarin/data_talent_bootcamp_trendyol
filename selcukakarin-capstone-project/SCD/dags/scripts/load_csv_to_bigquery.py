from google.cloud import bigquery
from google.oauth2 import service_account


def get_a_client():
    """
    Create client object to connect to google bigquery with json file

    :return: client => authorized BigQuery client object
    """
    # Get auth file to connect bigquery
    key_path = "/usr/local/airflow/dags/auth_files/dsmbootcamp-535dfd073f87.json"
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Create a bigquery client instance
    client = bigquery.Client(credentials=credentials, project=credentials.project_id, )
    return client


def load_csv_to_bigquery():
    """
    Read the data from the created csv file and transfer it to the big query environment
    """
    project = 'dsmbootcamp'
    dataset_id = 'selcuk_akarin'
    table_id = 'product_content'
    # Construct a BigQuery client object.
    table_ref = "{}.{}.{}".format(project, dataset_id, table_id)

    # Make a bigquery client
    client = get_a_client()

    # Create a job config instance to create bigquery schema
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.schema = [
        bigquery.SchemaField("product_content_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("product_content_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("category_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("category_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("subcategory_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("business_unit_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("business_unit_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("color", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("price", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("create_date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("update_date", "TIMESTAMP", mode="NULLABLE"),
    ]
    job_config.field_delimiter = ','
    job_config.allow_quoted_newlines = True
    job_config.encoding = 'UTF-8'
    job_config.autodetect = True

    # Product_content_data.csv path to get csv datas
    file_path = "/usr/local/airflow/dags/datas/product_content_data.csv"

    # Open and read product_content_data.csv
    with open(file_path, "rb") as file:
        load_job = client.load_table_from_file(
            file,
            table_ref,
            job_config=job_config
        )  # API request
        load_job.result()  # Waits for table load to complete.
    file.close()


if __name__ == "__main__":
    # Start load csv job
    load_csv_to_bigquery()
