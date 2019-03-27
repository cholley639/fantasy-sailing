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
        s_arr = scores_row[2:-2]
    else:
        s_arr = s.split(',')

    return s_arr


def main(scores_url, sailors_url):
    output_matrix = []
    sailors_matrix = sailors_scrapper.sailors_matrix(sailors_url)
    scores_matrix = full_scores_scrapper.scores_matrix(scores_url)

    max_num_races = scores_matrix[0][-3]
    reg_name = scores_matrix[1][-1]

    prev_skipper = ""
    prev_crew = ""
    for row in sailors_matrix[1:]:
        scores_row = []  # matches the correct scores for a given sailor from the scores_matrix
        for iter_score_row in scores_matrix[1:]:
            if iter_score_row[-1] == row[-1] and iter_score_row[1] == row[2]:
                scores_row = iter_score_row
                break
        print row[4], row[6], scores_row

        if row[4] != prev_skipper and row[6] != prev_crew:  # new skipper and crew
            skip_arr = [row[4], reg_name, row[1]]
            crew_arr = [row[6], reg_name, row[1]]

            skip_races = convert_races_string(row[5], scores_row)

            crew_races = convert_races_string(row[7], scores_row)
            # print skip_races
            # print crew_races

        elif row[4] != prev_skipper and row[6] == prev_crew:  # new skipper, same crew
            skip_arr = []

        else:  # same skipper, new crew
            crew_arr = []


if __name__ == '__main__':
    regatta_name = 'thompson'
    sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
    scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
    main(scores_url, sailors_url)
