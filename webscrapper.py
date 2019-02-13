"""
webscrapper.py

Cameron Holley
Feb 12 2019
fantasy-sailing

Practice using beautifulsoup to make a web scrapper


Possible useful classes - DIVISIONAL PAGE

 * table class="results coordinate division A"

 * class="schoolname"

 * class="sailor-name skipper"

 * class="totalcell"

Possible useful classes - FULL-SCORES PAGE
 * class="right"



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


def num_races(soup):

	num_races_list = []

	for races in soup.find_all(class_="right"):

		race_num = races.text

		if race_num == u'TOT':
			return len(num_races_list)

		num_races_list.append(race_num)

	return "ERROR COULDN'T FIND NUM_RACES"




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
    soup = import_page("f18", "coed-showcase", "full-scores")
    num_races = num_races(soup)

    print num_races





