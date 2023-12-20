from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound

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


def exec_scd_type_1():
    """

    """
    project = 'dsmbootcamp'
    dataset_id = 'selcuk_akarin'
    table_id = 'dim_product_content'
    # Construct a BigQuery client object.
    table_ref = "{}.{}.{}".format(project, dataset_id, table_id)

    # Make a bigquery client
    client = get_a_client()

    try:
        client.get_table(table_ref)  # Make an API request.
        print("Table {} already exists.".format(table_ref))
    except NotFound as error:
        print('Whoops! Table {} doesn\'t exist here! Ref: {}'.format(table_ref, error.grpc_status_code))
        # Make schema template for product_content table
        schema = [
            bigquery.SchemaField("product_content_sk", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("product_content_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("product_content_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("category_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("category_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("subcategory_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("business_unit_id", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("business_unit_name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("color", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("price", "FLOAT", mode="NULLABLE"),
            bigquery.SchemaField("etl_date_create", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("etl_date_update", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("is_deleted_in_source", "BOOLEAN", mode="NULLABLE"),
        ]

        # Create bigquery table
        table = bigquery.Table(table_ref, schema=schema)
        table = client.create_table(table)  # Make an API request.
        print(
            "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
        )
    finally:
        # Make a "slowly changing dimension type-1" with merge query
        QUERY = ("""
            MERGE `dsmbootcamp.selcuk_akarin.dim_product_content` t
            USING `dsmbootcamp.selcuk_akarin.product_content` s
            ON t.product_content_id = s.product_content_id
            WHEN MATCHED THEN UPDATE 
            SET t.product_content_id = s.product_content_id,
                t.product_content_name = s.product_content_name,
                t.category_id = s.category_id,
                t.category_name = s.category_name,
                t.subcategory_name = s.subcategory_name,
                t.business_unit_id = s.business_unit_id,
                t.business_unit_name = s.business_unit_name,
                t.color = s.color,
                t.price = s.price,
                is_deleted_in_source = False
                t.etl_date_update = CURRENT_TIMESTAMP()
            WHEN NOT MATCHED BY TARGET THEN
                insert (
                    product_content_sk,
                    product_content_id,
                    product_content_name,
                    category_id,
                    category_name,
                    subcategory_name,
                    business_unit_id,
                    business_unit_name,
                    color,
                    price,
                    etl_date_create,
                    etl_date_update,
                    is_deleted_in_source
                    )
                values (
                    FARM_FINGERPRINT(GENERATE_UUID()),
                    s.product_content_id,
                    s.product_content_name,
                    s.category_id,
                    s.category_name,
                    s.subcategory_name,
                    s.business_unit_id,
                    s.business_unit_name,
                    s.color,
                    s.price,
                    CURRENT_TIMESTAMP(),
                    CURRENT_TIMESTAMP(),
                    FALSE
                    )
            WHEN NOT MATCHED BY SOURCE THEN UPDATE 
            SET t.is_deleted_in_source = TRUE ;
            """)
        # Execute merge query
        query_job = client.query(QUERY)  # API request
        rows = query_job.result()  # Waits for query to finish
        print("Type 1 dimension is applied")
        for row in rows:
            print(row)


if __name__ == "__main__":
    # Execute SCD type-1 method
    exec_scd_type_1()
