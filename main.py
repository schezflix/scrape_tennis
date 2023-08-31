from scrape import scrape_tournament
from transform_tools import upload_to_s3

scrape_tournament('2019')

#upload_to_s3('tournament.csv')