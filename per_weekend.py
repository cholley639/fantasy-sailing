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

#TO DO:


import requests
from bs4 import BeautifulSoup
import csv
import sailors_scrapper
import full_scores_scrapper
import re


#constants

BREAKDOWN = u'BKD' # will be coded as a score of 999 == BREAKDOWN, give average


# Matches the races sailed for a given sailor with the results of those races. To be added to output row.
	# possible length combinations for the length of a race_set
		# 1 - 1 single digit race (ex. 5)
		# 2 - 1 double digit race (ex. 11)
		# 3 - single digit to single digit span (ex. 7-8)
		# 4 - single digit to double digit span (ex. 9-12)
		# 5 - double digit to double digit span (ex. 12-14)
def match_sailor_scores(s, scores_row, max_num_races):
	s_arr = [0] * max_num_races		# set all race scores to zero for max num of races in regatta

	if not s:
		for race_num in range(0, max_num_races):
			if scores_row[race_num] == BREAKDOWN:
				s_arr[race_num] = 999

			else:
				s_arr[race_num] = int(scores_row[race_num])

	else:
		races_sailed = s.split(',')	#array of races sailed 

		for race_set in races_sailed:		# race_set is either an individual race number,
											# 	or period of races donated ex. 9-12
			string_length = len(race_set)		# denotes length of the string, which can be used to categorize how to filter
			
			if string_length == 1 or string_length == 2:
				race_num = int(race_set)
				s_arr[race_num - 1] = int(scores_row[race_num - 1])	#replace the 0 for the race with the correct score


			elif string_length == 3:		# MIGHT NEED TO INCLUDE CASE WHERE race_set == RES on tech score
				first_race = int(race_set[0])
				last_race = int(race_set[2:])

				for race_num in range(first_race, last_race + 1):
					if scores_row[race_num -1] == BREAKDOWN:		# race score is a breakdown, write-off as 999 CONVERT LATER
						s_arr[race_num - 1] = 999

					else:
						s_arr[race_num - 1] = int(scores_row[race_num - 1])

			elif string_length == 4:
				first_race = int(race_set[0])
				last_race = int(race_set[2:])

				for race_num in range(first_race, last_race + 1):
					s_arr[race_num - 1] = int(scores_row[race_num - 1])
			
			else:	#string_length == 5
				first_race = int(race_set[0:2])
				last_race = int(race_set[3:])

				for race_num in range(first_race, last_race + 1):
					s_arr[race_num - 1] = int(scores_row[race_num - 1])

	return s_arr


# makes the headers row for the output array based on how many races were sailed in the regatta
def make_headers(max_num_races):
	headers = ['Name', 'Schoolref', 'Regatta', 'Div']

	for i in range(1, max_num_races + 1):
		headers.append(i)

	headers.append('Fantasy Points')

	return headers

# combines information to make each row that will be put into the output matrix
# the real reason for this function is to take the scores out of one arrray and transfer them
def make_final_output_rows(name, schoolref, regatta_name, div, scores_row):
	output_array = [name, schoolref, regatta_name, div]

	for i in scores_row:		#takes scores out of an array and inserts them
		output_array.append(i)

	return output_array

def main(scores_url, sailors_url, csv_file='weekend_results.csv'):
	output_matrix = []
	sailors_matrix = sailors_scrapper.sailors_matrix(sailors_url)
	scores_matrix = full_scores_scrapper.scores_matrix(scores_url)

	max_num_races = int(scores_matrix[0][-4])
	reg_name = scores_matrix[1][-2]

	headers = make_headers(max_num_races)
	#output_matrix.append(headers) 

	curr_skipper = ""
	curr_crew = ""
	for iter_sailor_row in sailors_matrix[1:]:		# iterates through rows in the sailors csv matrix
		match_score_row = []  							# creates empty row to be filled with the correct scores row for a given sailor(s)
		for iter_score_row in scores_matrix[1:]:	# iterates through rows in the scores csv matrix
			if iter_score_row[-1] == iter_sailor_row[0] and iter_score_row[1] == iter_sailor_row[3]: # matches the correct scores for a given sailor from the scores_matrix
				match_score_row = iter_score_row													 # first condition checks team, second checks division
				break

		if iter_sailor_row[5] != curr_skipper and iter_sailor_row[7] != curr_crew:  # new skipper and crew
			curr_skipper = iter_sailor_row[5]										# update latest seen skipper
			curr_crew = iter_sailor_row[7]											# update latest seen crew

			skip_races = match_sailor_scores(iter_sailor_row[6], match_score_row[2:-3], max_num_races)	 #race scores for all the races that the given sailor participated in
			crew_races = match_sailor_scores(iter_sailor_row[8], match_score_row[2:-3], max_num_races)

			skip_output_arr = make_final_output_rows(curr_skipper, iter_score_row[-1], reg_name, iter_sailor_row[3], skip_races)	#name, schoolref, regatta name, div, 
			crew_output_arr = make_final_output_rows(curr_crew, iter_score_row[-1], reg_name, iter_sailor_row[3], crew_races)

			output_matrix.append(skip_output_arr)
			output_matrix.append(crew_output_arr)

		elif iter_sailor_row[5] != curr_skipper and iter_sailor_row[7] == curr_crew:  # new skipper, same crew
			curr_skipper = iter_sailor_row[5]
			skip_races = match_sailor_scores(iter_sailor_row[6], match_score_row[2:-3], max_num_races)
			skip_output_arr = make_final_output_rows(curr_skipper, iter_score_row[-1], reg_name, iter_sailor_row[3], skip_races)
			output_matrix.append(skip_output_arr)

		else:  # same skipper, new crew
			curr_crew = iter_sailor_row[7]
			crew_races = match_sailor_scores(iter_sailor_row[8], match_score_row[2:-3], max_num_races)
			crew_output_arr = make_final_output_rows(curr_crew, iter_score_row[-1], reg_name, iter_sailor_row[3], crew_races)
			output_matrix.append(crew_output_arr)

	full_scores_scrapper.write_to_csv(csv_file, headers, output_matrix)



if __name__ == '__main__':
	regatta_name = 'thompson'
	sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
	scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
	main(scores_url, sailors_url)
