from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

#from azure.cosmos import CosmosClient
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from typing import Dict, Any
import json

# 1. Get your Primary Connection String
# You can find this in the Azure portal under your Cosmos DB account -> Keys.
# The connection string is in the format:
# AccountEndpoint=https://<your-account-name>.documents.azure.com:443/;AccountKey=<your-primary-key>;

# !!! IMPORTANT: Replace the placeholder with your actual connection string !!!
COSMOS_CONNECTION_STRING = "INSERT CONNECTION KEY" 
""
DATABASE_NAME = "ProdAI"
CONTAINER_NAME = "Sensor"

try:
    # Connect to the Azure Cosmos DB account using the connection string
    client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)
    
    print("Successfully connected to Azure Cosmos DB.")
    
    # Get a reference to a database
    #database = client.create_database(DATABASE_NAME)
    database = client.get_database_client(DATABASE_NAME)
    
    # Get a reference to a container (collection)
    partition_key = PartitionKey(path="/aiclass")
    #container = database.create_container(CONTAINER_NAME,partition_key )
    container = database.get_container_client(CONTAINER_NAME )

    new_item = {
    "id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
    "category": "gear-surf-surfboards",
    "name": "Yamba Surfboard",
    "quantity": 12,
    "sale": False,
    }

    created_item = container.upsert_item(new_item)

    existing_item = container.read_item(
        item="aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
        partition_key="gear-surf-surfboards",
        )
    print(existing_item)

    queryText = "SELECT * FROM products p WHERE p.category = @category"

    results = container.query_items(
        query=queryText,
        parameters=[
        dict(
            name="@category",
            value="gear-surf-surfboards",
            )
        ],
        enable_cross_partition_query=False,)  

    items = [item for item in results]

    output = json.dumps(items, indent=True) 
    print(output)


    
    # Example operation: Query items
    query = "SELECT * FROM c WHERE c.id = '1'"
    print(f"\nExecuting query: {query}")
    
    # QueryItems returns an iterable of the resulting documents
    items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
    ))
    
    if items:
        print(f"Found {len(items)} item(s).")
        print("First item ID:", items[0].get('id'))
    else:
        print("No items found matching the query.")
    
except Exception as e:
    print(f"An error occurred: {e}")