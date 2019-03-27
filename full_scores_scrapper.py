"""
full_scores_scrapper.py

Cameron Holley
Winter 2019

This is a program for my fantasy-sailing web app project.
This file contains the implementation for a webscrapper using BeautifulSoup
that takes all of the data I need from the full-scores page of a given college
sailing regatta on the techscore website.

The functions main() and scores_matrix() are very similar. The difference
is that main() is used to test the functioanlity and output the resulting
data to a csv. Meanwhile, scores_matrix() is the actual function being imported
by in the back-end of the app that delivers the data as a matrix to other
python functions.

"""


import requests
from bs4 import BeautifulSoup
import csv
import re



#Param: string url
#Returns: raw text
#Does: returns raw html from a given url
def get_html_from_url(url):
    res = requests.get(url)
    return res.text


#Param: output file name, headers row, output data
#Returns: n/a
#Does: writes the data to a csv with
#       the first row as headers
def write_to_csv(file_name, headers, data):
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        for row in data:
            csv_writer.writerow(row)


#Param: string url
#Returns: data in matrix form with headers as first row
#Does: Scrapes the /full-scores/ page of any techscore regatta
#       for all of the sailing data from that given regatta.
#       Formats the data as a 2D-array (matrix)
def scores_matrix(url):
    raw_html = get_html_from_url(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    data = []
    scores_table = soup.find('table', attrs={'class': 'results coordinate'})
    scores_body = scores_table.find('tbody')

    temp_header1 =  scores_table.find('thead').find('tr').find_all('th')[2:-2]
    temp_header2 = scores_table.find('thead').find('tr').find_all('th')[-1:]
    scores_headers = temp_header1 + temp_header2
    headers = [ele.text.strip() for ele in scores_headers]
    headers.append("Regatta")
    headers.append('schoolref')
    reg_name = soup.find('span', attrs={'itemprop': 'name'}).text

    #add name to headers rank

    rows = scores_body.find_all('tr')
    teamname = ""
    schoolref = None
    for row in rows:
        if 'totalrow' not in row['class']:
            if 'divA' in row['class']:
                teamname = row.find_all('td')[2].text
                schoolref = row.find_all('td')[2].find('a')['href']

            arr = []
            count=0
            for ele in row.find_all('td')[2:]:
                if count==0:
                    arr.append(teamname)
                elif ele == row.find_all('td')[-2]:
                    pass
                else:
                    arr.append(ele.text)
                count+=1

            arr.append(reg_name)
            arr.append(schoolref)
            data.append(arr)

    data.insert(0, headers)

    return data


#   same as scores_matrix, but used to test functionality
#   and write to csv directly (see notes at top)
def main(url, csv_file='scores.csv'):
    raw_html = get_html_from_url(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    data = []
    scores_table = soup.find('table', attrs={'class': 'results coordinate'})
    scores_body = scores_table.find('tbody')

    temp_header1 =  scores_table.find('thead').find('tr').find_all('th')[2:-2]
    temp_header2 = scores_table.find('thead').find('tr').find_all('th')[-1:]
    scores_headers = temp_header1 + temp_header2
    headers = [ele.text.strip() for ele in scores_headers]
    headers.append("Regatta")
    headers.append('schoolref')
    reg_name = soup.find('span', attrs={'itemprop': 'name'}).text


    #add name to headers rank

    rows = scores_body.find_all('tr')
    teamname = ""
    schoolref = None
    for row in rows:
        if 'totalrow' not in row['class']:
            if 'divA' in row['class']:
                teamname = row.find_all('td')[2].text
                schoolref = row.find_all('td')[2].find('a')['href']

            arr = []
            count=0
            for ele in row.find_all('td')[2:]:
                if count==0:
                    arr.append(teamname)
                elif ele == row.find_all('td')[-2]:
                    pass
                else:
                    arr.append(ele.text)
                count+=1

            arr.append(reg_name)
            arr.append(schoolref)

            data.append(arr)
            #data.append([ele.text for ele in row.find_all('td')])

    write_to_csv(csv_file, headers, data)


if __name__ == '__main__':
    regatta_name = 'thompson'
    techscore_url = 'https://scores.collegesailing.org/s18/{}/full-scores/'.format(regatta_name)
    main(techscore_url)


