"""
regatta_class.py

Implementation for regatta class
fantasy-sailing


Cameron Holley
"""


import math
import os
import numpy as np 
from bs4 import BeautifulSoup
import webscrapper as ws



def make_FR_Regatta(Ascore, Bscore, Ateam, Bteam, num_races):
	return	Ascore


#Class representing a fleet race regatta

class FR_Regatta:

	#def __init__(self, season, name):
	#	self.season = season
	#	self.name = name

	def __init__(self, link):
		self.link = link
		tmp = link.split("/")
		tmp = filter(None, tmp)
		self.season = str(tmp[2])
		self.name = str(tmp[3])

		self.soupA = ws.import_page(self.season, self.name, "A")
		self.soupB = ws.import_page(self.season, self.name, "B")
		self.soupFS = ws.import_page(self.season, self.name, "full-scores")

	def team_listA(self):
		return ws.get_teams_list(self.soupA)

	def team_listB(self):
		return ws.get_teams_list(self.soupB)

	def score_listA(self):
		return ws.get_scores_list(self.soupA)

	def score_listB(self):
		return ws.get_scores_list(self.soupB)

	def num_races(self):
		return ws.num_races(self.soupFS)

     	""" r = requests.get(link) #+ "rotations")

      	data = r.text

      	soup = BeautifulSoup(data)

      	table = soup.find('tbody')

      	if table:
         	rows = table.find_all("tr")
        	for row in rows:
            	order = 0
            	school = ""
            	teamname = ""
            	totalScore = "N/A"
            	cols = row.find_all("td")
            	for col in cols:
               		if order == 3:
                  		school = col.text
               		elif order == 4:
                  		teamname = col.text
               		elif order == 9:
                  		totalScore = col.text
            # self.teams.append({'name': cols[0]})
               order = order + 1
            self.teams.append({'name': teamname, 'school': school, 'score': totalScore})
            # for col in cols:
            #    # self.teams.append({'name': col.text})
            #    self.teams.append({'name': col.text})
      	else:
         	self.teams.append("Teams not available")



   	def to_json(self):
      	return {
         	'name': self.name,
         	'label': self.label,
         	# 'host': self.host,
         	'link': self.link,
         	'teams': self.teams
      	}

	"""



if __name__ == '__main__':
	url = "https://scores.collegesailing.org/f18/coed-showcase/"
	cpt_hurst = FR_Regatta(url)
	print cpt_hurst.score_listB()
	print cpt_hurst.score_listA()
	print cpt_hurst.num_races()


	
