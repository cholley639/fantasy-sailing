import requests
from bs4 import BeautifulSoup
import csv



def get_html_from_url(url):
    res = requests.get(url)
    return res.text


def write_to_csv(file_name, headers, data):
    with open(file_name, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        for row in data:
            csv_writer.writerow(row)


def sailors_matrix(url):
    raw_html = get_html_from_url(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    data = []
    sailors_table = soup.find('table', attrs={'class': 'coordinate sailors'})
    sailors_body = sailors_table.find('tbody')

    sailors_headers = sailors_table.find('thead').find('tr').find_all('th')
    headers =  ['schoolref'] + [ele.text.strip() for ele in sailors_headers]
    headerKeys = ['schoolref', 'schoolname', 'teamname', 'division-cell', 'rank-cell', 'skipper', 'sraces', 'crew', 'craces']

    rows = sailors_body.find_all('tr')
    field_names = ['skipper', 'sraces', 'crew', 'craces']

    curr_data = {}
    schoolref = None
    for row in rows:
        if 'topborder' in row['class']:
            curr_data = {}

        if 'reserves-row' not in row['class']:

            for field in row.find_all('td')[:-4]:
                if field.text.strip() and field['class'][0] == 'schoolname':
                    curr_data['schoolref'] = field.find('a')['href']
                if field.text.strip():
                    curr_data[''.join(field['class'])] = field.text.strip()

            for field, name in zip(row.find_all('td')[-4:], field_names):
                if field.text.strip() or name not in curr_data:
                    curr_data[name] = field.text.strip()

            new_list = [curr_data[key] for key in headerKeys]
            data.append(new_list)

    data.insert(0, headers)

    return data


def main(url, csv_file='sailors.csv'):
    raw_html = get_html_from_url(url)
    soup = BeautifulSoup(raw_html, 'html.parser')

    data = []
    sailors_table = soup.find('table', attrs={'class': 'coordinate sailors'})
    sailors_body = sailors_table.find('tbody')

    sailors_headers = sailors_table.find('thead').find('tr').find_all('th')
    headers = ['schoolref'] + [ele.text.strip() for ele in sailors_headers]
    headerKeys = ['schoolref', 'schoolname', 'teamname', 'division-cell', 'rank-cell', 'skipper', 'sraces', 'crew', 'craces']

    rows = sailors_body.find_all('tr')
    field_names = ['skipper', 'sraces', 'crew', 'craces']

    curr_data = {}
    schoolref = None
    for row in rows:
        if 'topborder' in row['class']:
            curr_data = {}

        if 'reserves-row' not in row['class']:

            for field in row.find_all('td')[:-4]:
                if field.text.strip() and field['class'][0] == 'schoolname':
                    curr_data['schoolref'] = field.find('a')['href']
                if field.text.strip():
                    curr_data[''.join(field['class'])] = field.text.strip()

            for field, name in zip(row.find_all('td')[-4:], field_names):
                if field.text.strip() or name not in curr_data:
                    curr_data[name] = field.text.strip()

            new_list = [curr_data[key] for key in headerKeys]
            data.append(new_list)

    write_to_csv(csv_file, headers, data)


if __name__ == '__main__':
    regatta_name = 'thompson'
    techscore_url = 'https://scores.collegesailing.org/s18/{}/sailors/'.format(regatta_name)
    main(techscore_url)
