"""
sailor_score_per_weekend.py

This function/file will be responsible for combining the two data tables
from the sailors techscore page and the full-scores tech score page.

Final product should look like this:

cont DIDNOTSAIL = 0

 sailor 		|	div	|race 1 | race 2 | .... | TOT
 --------------------------------------------
 Jack Bitney 	|	B 	|	0	|	0	|	0	|	0	|	0	|	0	|	0	|	0	|	0	|	0	|	6	|	2	|	8	|


"""


import requests
from bs4 import BeautifulSoup
import csv
import sailors_scrapper

def main(scores_url, sailors_url):
	sailor_matrix = sailors_scrapper.sailors_matrix(sailors_url)

	scores_matrix = 

if __name__ == '__main__':
    regatta_name = 'thompson'
    sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
    scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
    main(scores_url, sailors_url)

