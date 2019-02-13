"""
webscrapper.py

Cameron Holley
Feb 12 2019
fantasy-sailing

Practice using beautifulsoup to make a web scrapper


possible useful classes

table class="results coordinate division A"

class="schoolname"

class="sailor-name skipper"

class="totalcell"



*** The number of teams in the event can be determined by the length of the lists***
"""

from bs4 import BeautifulSoup
import requests

def import_page(season, regatta, div):
	unique_string = season + "/" + regatta + "/" + div + "/"
	r = requests.get("http://scores.collegesailing.org/" + unique_string)
	data = r.text
	soup = BeautifulSoup(data, "lxml")

	return soup


def get_scores_list(soup):

	scores_list = []

	for scores in soup.find_all(class_='totalcell'):

		num = scores.text
		scores_list.append(num)

	return scores_list


def get_teams_list(soup):

	teams_list = []

	for teams in soup.find_all(class_='schoolname'):
		name = teams.text
		teams_list.append(name)

	return teams_list





if __name__ == '__main__':
    soup = import_page("f18", "coed-showcase", "A")

    scores_list = get_scores_list(soup)
    teams_list = get_teams_list(soup)

    print len(teams_list)





