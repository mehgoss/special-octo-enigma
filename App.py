import pymongo
import os
from urllib.parse import quote_plus

def connect_to_atlas():
    try:
        # Retrieve connection details from environment variables
        username = os.getenv("MONGODB_ATLAS_USERNAME")
        password = os.getenv("MONGODB_ATLAS_PASSWORD")
        cluster = os.getenv("MONGODB_ATLAS_CLUSTER")
        
        if not all([username, password, cluster]):
            raise ValueError("Missing one or more required environment variables: MONGODB_ATLAS_USERNAME, MONGODB_ATLAS_PASSWORD, MONGODB_ATLAS_CLUSTER")
        
        # Construct the connection string
        connection_string = f"mongodb+srv://{quote_plus(username)}:{quote_plus(password)}@{cluster}.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        # Connect to MongoDB Atlas
        client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.admin.command("ping")  # Sends a ping to confirm a successful connection
        print("Successfully connected to MongoDB Atlas!")
        
        # Get and display list of databases
        databases = client.list_database_names()
        print("\nAvailable databases:")
        for db in databases:
            print(f"- {db}")
        
        return client
    
    except pymongo.errors.ConnectionError as e:
        print(f"Connection error: {e}")
        return None
    except pymongo.errors.ConfigurationError as e:
        print(f"Configuration error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if 'client' in locals():
            client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    connect_to_atlas()
