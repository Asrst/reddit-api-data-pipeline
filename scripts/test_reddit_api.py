import pandas as pd
import praw
import os, sys
from datetime import datetime

REDDIT_CLIENT_ID = os.environ.get('REDDIT_CLIENT_ID')
REDDIT_SECRET = os.environ.get('REDDIT_SECRET')


def fetch_data(subreddit):
    """Extract Data to Pandas DataFrame object"""

    client = praw.Reddit(
            client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET, 
            user_agent="top-posts-fetcher")
    
    post_items = []
    try:
        subreddit = client.subreddit(subreddit)
        posts = subreddit.top(time_filter=TIME_FILTER, limit=None)
        for submission in posts:
            to_dict = vars(submission)
            # print(to_dict['url'], to_dict['permalink'])
            sub_dict = {field: to_dict[field] for field in POST_FIELDS}
            post_items.append(sub_dict)
            out_df = pd.DataFrame(post_items)
    except Exception as e:
        print(f"Exception Ocurred:{e}")
        sys.exit(1)

    return out_df


def transform(df):
    """Apply basic transformation to the extracted data."""
    # Convert epoch to UTC
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    
    return df 


def upload_df_to_gcs(df, bucket_name, save_path) -> None:
    """Upload data frame to GCS"""

    from google.cloud import storage

    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    
    # storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    # storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

    # initialize gcs client
    client = storage.Client()
    # The bucket on GCS in which to write the CSV file
    bucket_obj = client.bucket(bucket_name)
    # The name assigned to the CSV file on GCS
    blob = bucket_obj.blob(save_path)
    blob.upload_from_string(df.to_csv(index=False), 'text/csv')

    return


def run_etl(subreddit, bucket_name, save_path):
    """Extract Reddit data and load to CSV"""
    data_df = fetch_data(subreddit)
    data_df = transform(data_df)
    print("# of data points: ", data_df.shape)
    upload_df_to_gcs(data_df, bucket_name, save_path)


if __name__ == "__main__":
    # gcp bucket to store the data.
    GCP_GCS_BUCKET="dl-reddit-api-404"
    # Variables for extracting data from reddit API (PRAW)
    SUBREDDIT = "ipl"
    TIME_FILTER = "month"
    POST_FIELDS = (
        "id",
        "title",
        "score",
        "num_comments",
        "author",
        "created_utc",
        "url",
        "upvote_ratio",
        "over_18",
        "edited",
        "spoiler",
        "stickied",
    )

    dt_now = datetime.now().strftime("%Y%m%d")
    OUTPUT_PATH = f"{SUBREDDIT}/test/top-posts-{dt_now}.csv"
    run_etl(SUBREDDIT, GCP_GCS_BUCKET, OUTPUT_PATH)
