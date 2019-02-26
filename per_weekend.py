"""
sailor_score_per_weekend.py

This function/file will be responsible for combining the two data tables
from the sailors techscore page and the full-scores tech score page.

Final product should look like this:

cont DIDNOTSAIL = 0

 sailor 		|	reg	|	div	|race 1 | race 2 | .... |race 11|race12 |	TOT | fantasy points
 --------------------------------------------
 Jack Bitney 	|thompson|	B	|	0	|	0	 | ....	|	6	|	2	|	8	| 


"""


import requests
from bs4 import BeautifulSoup
import csv
import sailors_scrapper
import full_scores_scrapper
import re


def convert_races(s):
	s_arr = s.split(',')
	return s_arr

def main(scores_url, sailors_url):
	output_matrix = []
	sailors_matrix = sailors_scrapper.sailors_matrix(sailors_url)
	scores_matrix = full_scores_scrapper.scores_matrix(scores_url)

	prev_skipper = ""
	prev_crew = ""
	for row in sailors_matrix[1:]:
		if row[4] != prev_skipper and row[6] != prev_crew:		#new skipper and crew
			skip_arr = [row[4], scores_matrix[1][-1], row[2]]
			crew_arr = [row[6], scores_matrix[1][-1], row[2]]

			skip_races = convert_races(row[5])
			crew_races = convert_races(row[7])
			print skip_races
			print crew_races


		elif row[4] != prev_skipper and row[6] == prev_crew:	#new skipper, same crew
			skip_arr = []

		else: 													#same skipper, new crew
			crew_arr = []


if __name__ == '__main__':
    regatta_name = 'thompson'
    sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
    scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
    main(scores_url, sailors_url)

