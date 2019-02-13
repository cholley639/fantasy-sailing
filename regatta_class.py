"""
regatta_class.py

Implementation for regatta class
fantasy-sailing


Cameron Holley
"""


import math
import os
import numpy as np 
import webscrapper as ws


#Class representing a fleet race regatta

class FR_Regatta:

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



if __name__ == '__main__':
	url = "https://scores.collegesailing.org/f18/coed-showcase/"
	cpt_hurst = FR_Regatta(url)


	
