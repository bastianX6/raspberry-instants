# Keys

Here you must place two configurations files:
- gc_key.json : Your google cloud key
- gc_data.json: This file contains some configurations in the following format:

```json
{
    "firestore": {
        "collection_name": "<your_collection_name>",
        "field_name": "songs"
    },
    "cloud_storage" : {
        "bucket_name" : "<your_bucket_name>",
        "file_prefix" : "<your_file_prefix>"
    }
}
```
