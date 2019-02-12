"""
webscrapper.py

Cameron Holley
Feb 12 2019
fantasy-sailing

Practice using beautifulsoup to make a web scrapper
"""


from bs4 import BeautifulSoup
import requests



def get_div_scores(season, regatta, div):
	r = requests.get("http://scores.collegesailing.org/" + season + regatta)
	data = r.text
	soup = BeautifulSoup(data)



if __name__ == '__main__':
    get_div_scores(f18, coed-showcase, A)
    
