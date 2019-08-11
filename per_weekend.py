"""
sailor_score_per_weekend.py

This function/file will be responsible for combining the two data tables
from the sailors techscore page and the full-scores tech score page.

Final product should look like this:

cont DIDNOTSAIL = 0

 sailor 		| team	|	reg	 |	div	|race 1 | race 2 | .... |race 11|race12 |	TOT | fantasy points
 --------------------------------------------
 Jack Bitney 	| Tufts	|thompson|	B	|	0	|	0	 | ....	|	6	|	2	|	8	| 


"""

import requests
from bs4 import BeautifulSoup
import csv
import sailors_scrapper
import full_scores_scrapper
import re


# converts string indicating what races were sailed to easier format
def convert_races_string(s, scores_row):
    if not s:  # all races sailed
        s_arr = scores_row[2:-3]
    else:
        s_arr = s.split(',')

    return s_arr


def main(scores_url, sailors_url):
    output_matrix = []
    sailors_matrix = sailors_scrapper.sailors_matrix(sailors_url)
    scores_matrix = full_scores_scrapper.scores_matrix(scores_url)

    max_num_races = scores_matrix[0][-4]
    reg_name = scores_matrix[1][-2]
    print max_num_races
    print reg_name

    prev_skipper = ""
    prev_crew = ""
    for iter_sailor_row in sailors_matrix[1:]:		# iterates through rows in the sailors csv matrix
        match_score_row = []  							# creates empty row to be filled with the correct scores row for a given sailor(s)
        for iter_score_row in scores_matrix[1:]:	# iterates through rows in the scores csv matrix
            if iter_score_row[-1] == iter_sailor_row[0] and iter_score_row[1] == iter_sailor_row[2]: # matches the correct scores for a given sailor from the scores_matrix
                match_score_row = iter_score_row									 				# first condition checks team, second checks division
                break

        if iter_sailor_row[5] != prev_skipper and iter_sailor_row[7] != prev_crew:  # new skipper and crew
            skip_arr = [iter_sailor_row[5], reg_name, iter_score_row[-1]]		
            crew_arr = [iter_sailor_row[7], reg_name, iter_score_row[-1]]

            

            skip_races = convert_races_string(iter_sailor_row[6], match_score_row)

            crew_races = convert_races_string(iter_sailor_row[8], match_score_row)
            print skip_races
            print crew_races
            

        elif iter_sailor_row[5] != prev_skipper and iter_sailor_row[7] == prev_crew:  # new skipper, same crew
            skip_arr = []

        else:  # same skipper, new crew
            crew_arr = []


if __name__ == '__main__':
    regatta_name = 'thompson'
    sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
    scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
    main(scores_url, sailors_url)
