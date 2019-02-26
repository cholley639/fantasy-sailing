import requests
from bs4 import BeautifulSoup
import csv
import re



def get_html_from_url(url):
    res = requests.get(url)
    return res.text


def write_to_csv(file_name, headers, data):
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        for row in data:
            csv_writer.writerow(row)


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

    #add name to headers rank

    rows = scores_body.find_all('tr')
    teamname = ""
    for row in rows:
        if 'totalrow' not in row['class']:
            if 'divA' in row['class']:
                teamname = row.find_all('td')[2].text

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

            data.append(arr)
    data.insert(0, headers)

    return data

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

    #add name to headers rank

    rows = scores_body.find_all('tr')
    teamname = ""
    for row in rows:
        if 'totalrow' not in row['class']:
            if 'divA' in row['class']:
                teamname = row.find_all('td')[2].text

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

            data.append(arr)
            #data.append([ele.text for ele in row.find_all('td')])

    write_to_csv(csv_file, headers, data)


if __name__ == '__main__':
    regatta_name = 'thompson'
    techscore_url = 'https://scores.collegesailing.org/s18/{}/full-scores/'.format(regatta_name)
    main(techscore_url)


