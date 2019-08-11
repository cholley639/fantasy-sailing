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


# Matches the races sailed for a given sailor with the results of those races. To be added to output row.
    # possible length combinations for the length of a race_set
        # 1 - 1 single digit race (ex. 5)
        # 2 - 1 double digit race (ex. 11)
        # 3 - single digit to single digit span (ex. 7-8)
        # 4 - single digit to double digit span (ex. 9-12)
        # 5 - double digit to double digit span (ex. 12-14)
def match_sailor_scores(s, scores_row):
    if not s:  # all races sailed
        s_arr = scores_row

    else:
        race_nums = s.split(',')	#array of race_sets sailed 

        for race_set in race_nums:		# race_set is either an individual race number,
        								# 	or period of races donated ex. 9-12
        	set_length = len(race_set)
        	
        	if set_length == 1 or set_length == 2:
        		s_arr = [scores_row[int(race_set) - 1]]

        	elif set_length == 3:		# MIGHT NEED TO INCLUDE CASE WHERE RACE_SET == RES on tech score
        		s_arr = scores_row[int(race_set[0])-1: int(race_set[2])]

        	elif set_length == 4:
        		s_arr = scores_row[int(race_set[0])-1: int(race_set[2:])]
        	
        	else:
        		s_arr = scores_row[int(race_set[0:2])-1: int(race_set[3:])]

    return s_arr


def main(scores_url, sailors_url):
    output_matrix = []
    sailors_matrix = sailors_scrapper.sailors_matrix(sailors_url)
    scores_matrix = full_scores_scrapper.scores_matrix(scores_url)

    max_num_races = scores_matrix[0][-4]
    reg_name = scores_matrix[1][-2]

    curr_skipper = ""
    curr_crew = ""
    for iter_sailor_row in sailors_matrix[1:]:		# iterates through rows in the sailors csv matrix
        match_score_row = []  							# creates empty row to be filled with the correct scores row for a given sailor(s)
        for iter_score_row in scores_matrix[1:]:	# iterates through rows in the scores csv matrix
            if iter_score_row[-1] == iter_sailor_row[0] and iter_score_row[1] == iter_sailor_row[3]: # matches the correct scores for a given sailor from the scores_matrix
                match_score_row = iter_score_row													 # first condition checks team, second checks division
                break

        if iter_sailor_row[5] != curr_skipper and iter_sailor_row[7] != curr_crew:  # new skipper and crew
        	skip_output_row = []
        	crew_output_row = []

        	curr_skipper = iter_sailor_row[5]										# update latest seen skipper
        	curr_crew = iter_sailor_row[7]											# update latest seen crew

        	skip_races = match_sailor_scores(iter_sailor_row[6], match_score_row[2:-3])	 #race scores for all the races that the given sailor participated in
        	crew_races = match_sailor_scores(iter_sailor_row[8], match_score_row[2:-3])

        	
			# TO DO: MAKE THE SKIP_RACES AND CREW_RACES ALL THE SAME LENGTH WITH THE TOTAL NUMBER OF RACES
			# AND HAVE ALL THE RACES THAT HE/SHE DIDN'T SAIL BE 0 SO THAT ALL ARRAYS ARE THE SAME LENGTH

			# Currently the array sizes are just the length of the number of races sailed        		
        	


        	skip_arr = [curr_skipper, iter_score_row[-1], reg_name, iter_sailor_row[1]]	#name, schoolref, regatta name, div, 
        	crew_arr = [curr_crew, iter_score_row[-1], reg_name, iter_sailor_row[1]]

        elif iter_sailor_row[5] != curr_skipper and iter_sailor_row[7] == curr_crew:  # new skipper, same crew
            skip_arr = []

        else:  # same skipper, new crew
            crew_arr = []


if __name__ == '__main__':
    regatta_name = 'thompson'
    sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
    scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
    main(scores_url, sailors_url)
