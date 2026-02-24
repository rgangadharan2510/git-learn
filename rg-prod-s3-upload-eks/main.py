import argparse
import logging
from src.s3_utils import upload_file, download_file
from src.json_utils import read_json, print_summary
import time

DEFAULT_BUCKET = "rg-python-refresh"
FILE_NAME = "data.json"
DOWNLOADED_FILE = "downloaded_data.json"


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="S3 JSON DevOps Tool")

    parser.add_argument("--upload", action="store_true", help="Upload JSON to S3")
    parser.add_argument("--download", action="store_true", help="Download JSON from S3")
    parser.add_argument("--bucket", default=DEFAULT_BUCKET, help="S3 bucket name")

    args = parser.parse_args()

    if args.upload:
        upload_file(args.bucket, FILE_NAME)

    elif args.download:
        download_file(args.bucket, FILE_NAME, DOWNLOADED_FILE)
        data = read_json(DOWNLOADED_FILE)
        print_summary(data)
        while True:
          time.sleep(60)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
