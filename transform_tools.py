import re
import pandas as pd
import boto3
import os




def regex_striper(string:str) -> str:
    string = re.sub('\r', '',string).strip()
    string = re.sub('\n', '',string).strip()
    string = re.sub('\t', '',string).strip()
    string = re.sub('-', '',string).strip()

    return string

def set_transformer(match):
    partido = []
    for set_t in match:
        if len(set_t) == 3:
            partido.append('-'.join(set_t[:2]))
            continue
        else:
            partido.append('-'.join(set_t))
    return partido


def csv_converter(data:dict, name:str) -> pd.DataFrame:
    return pd.DataFrame(data).to_csv(f"csv/{name}.csv", index=False)


def upload_to_s3(file) -> None:
    try:
        s3 = boto3.resource(
            service_name = "s3",
            region_name = "us-west-1",
            aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        s3.Bucket("schezflix-glue-etl").upload_file(Filename=file, Key=file)
        print('CSV file successfuly uploaded to S3.')

    except ConnectionError:
        raise ConnectionError('Something wrong happened with the connection to S3.')

