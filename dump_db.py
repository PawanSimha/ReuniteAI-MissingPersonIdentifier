import json
from pymongo import MongoClient
from bson import json_util
import os
from dotenv import load_dotenv

load_dotenv()

def dump_database():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DB_NAME = os.getenv("DB_NAME", "reuniteai_db")
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        # Check connection
        client.admin.command('ping')
        print(f"Connected to MongoDB: {DB_NAME}\n")
        
        db = client[DB_NAME]
        collections = ["users", "face_encodings", "missing_persons"]
        
        for coll_name in collections:
            print(f"--- Collection: {coll_name} ---")
            coll = db[coll_name]
            cursor = coll.find({})
            count = 0
            for doc in cursor:
                # Use bson.json_util to handle MongoDB specific types like ObjectId, datetime
                print(json.dumps(doc, indent=2, default=json_util.default))
                print("-" * 20)
                count += 1
            
            if count == 0:
                print("No data found in this collection.")
            else:
                print(f"Total documents: {count}")
            print("\n")
            
    except Exception as e:
        print(f"Error connecting to or reading from database: {e}")

if __name__ == "__main__":
    dump_database()
