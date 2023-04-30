import pandas as pd
import praw
import os, sys
from datetime import datetime
from pmaw import PushshiftAPI
from dateutil import parser
from dateutil.relativedelta import relativedelta

# field names to extract from the API response.
POST_FIELDS = (
        "id",
        "title",
        "score",
        "num_comments",
        "author",
        "author_flair_type",
        "author_premium",
        "created_utc",
        "url",
        "upvote_ratio",
        "over_18",
        "edited",
        "spoiler",
        "stickied",
        "num_crossposts",
        "is_crosspostable",
        "content_categories",
        "archived",
        "post_hint",
        "media",
        "gilded",
        "selftext",
    )

def fetch_data(subreddit, start, end):
    """Extract Data to Pandas DataFrame object"""

    client = PushshiftAPI()
    
    post_items = []
    try:
        # end date is not inclusive
        posts = client.search_submissions(subreddit=subreddit, limit=None, 
                                            since=start, until=end)
        if len(posts) < 1:
            return pd.DataFrame()

        for post in posts:
            # print(post['url'], post['permalink'])
            sub_dict = {field: post.get(field, None) for field in POST_FIELDS}
            post_items.append(sub_dict)
    except Exception as e:
        print(f"Exception Ocurred:{e}")
        sys.exit(1)

    out_df = pd.DataFrame(post_items)
    return out_df


def transform(df):
    """Apply basic transformation to the extracted data."""
    
    # Convert epoch to UTC
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    
    # check for media
    df["has_media"] = df['media'].apply(lambda x: False if x is None else True)
    
    # join if categories are multiple
    isna = df['content_categories'].isna()
    df.loc[isna, 'content_categories'] = df.loc[isna, 'content_categories'].apply(lambda x: [])
    df["content_categories"] = df["content_categories"].apply(",".join)
    
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


def run_etl(subreddit, year_month, bucket_name):
    """Extract Reddit data and load to CSV"""

    year, month = year_month.split("-")
    start_date = parser.parse(f"{year}-{month}-01")
    end_date = start_date + relativedelta(months=1)
    print(f"#start: {start_date}, #end: {end_date}")

    start_epoch = int(start_date.timestamp())
    end_epoch = int(end_date.timestamp())

    data_df = fetch_data(subreddit, start_epoch, end_epoch)
    data_df = transform(data_df)
    print("# of data points: ", data_df.shape)

    save_path = f"{subreddit}/posts-{year_month}.csv"
    upload_df_to_gcs(data_df, bucket_name, save_path)


if __name__ == "__main__":
    # GCP bucket to store data
    GCP_GCS_BUCKET="dl-reddit-api-404"

    # Variables for extracting data from reddit API (PRAW)
    SUBREDDIT = "technology"

    years = [2022]
    months = list(range(1, 13))

    for year in years:
        for month in months:
            year_month = f"{year}-{month}"
            print("running etl for: ", year_month)
            run_etl(SUBREDDIT, year_month, GCP_GCS_BUCKET)
            print("#"*70)
