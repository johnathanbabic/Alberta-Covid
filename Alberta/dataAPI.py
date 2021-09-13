# This program will be used to download data files from the 
# governemnt of alberta website. These data files will later
# be used in other python programs. 

import requests
import sys
import os

def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def main():

    if os.path.exists("covid-19-alberta-statistics-data.csv"):
        os.remove("covid-19-alberta-statistics-data.csv")
        download_file("https://www.alberta.ca/data/stats/covid-19-alberta-statistics-data.csv")
    else:
        download_file("https://www.alberta.ca/data/stats/covid-19-alberta-statistics-data.csv")
    
    if os.path.exists("lga-coverage.csv"):
        os.remove("lga-coverage.csv")
        download_file("https://www.alberta.ca/data/stats/lga-coverage.csv")
    else:
        download_file("https://www.alberta.ca/data/stats/lga-coverage.csv")

    """
    elif sys.argv[1] == "Canada":
        
        if os.path.exists("vaccination-coverage-map.csv"):
            os.remove("vaccination-coverage-map.csv")
            download_file("https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-map.csv")
        else:
            download_file("https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-map.csv")

        if os.path.exists("covid19-download.csv"):
            os.remove("covid19-download.csv")
            download_file("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv")
        else:
            download_file("https://health-infobase.canada.ca/src/data/covidLive/covid19-download.csv")
    """


main()