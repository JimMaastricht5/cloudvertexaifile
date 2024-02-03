from google.cloud import storage
import pandas as pd

BUCKET='tweetersp2'
DELIMITER='/'
PREFIX_REAL_WORLD='real-world/'
PREFIX_AI_GENERATED='ai-generated/'
FOLDERS = [PREFIX_REAL_WORLD, PREFIX_AI_GENERATED]

# BASE_PATH = f'gs://{BUCKET}/{PREFIX}'

print(f'BUCKET : {BUCKET}')
print('Connecting to GCP Storage')
client = storage.Client()
bucket = client.get_bucket(BUCKET)


print('Fetching list of objects to generate the import file')

data = []

for folder in FOLDERS :

    blobs = client.list_blobs(BUCKET, prefix=folder, delimiter=DELIMITER)

    for blob in blobs:
        # range to remove the last character which is a delimiter
        label = folder[:-1] 
        data.append({
            'FILE_PATH': f'gs://{BUCKET}/{blob.name}',
            'LABEL': label
        })


df = pd.DataFrame(data)

print('Exporting import file data to CSV-file')
df.to_csv('import_file_faces.csv', index=False, header=False)

# Instantiates a client
storage_client = storage.Client()

# Get GCS bucket
bucket = storage_client.get_bucket(BUCKET)

# Get blobs in bucket (including all subdirectories)
blobs_all = list(bucket.list_blobs())

# Get blobs in specific subirectory
blobs_specific = list(bucket.list_blobs(prefix='path/to/subfolder/'))
