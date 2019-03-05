# Fantasy College Sailing

## Current Status

So far, this repository has the webscrappings tools for fleet race regattas. It can successfully pull the sailors page and full-scores page of any regatta on the techscore website. The next step is combining the two pages to be uploaded to the league pool database.

## Drafting

Current thought is that we will start with a fixed league size, say 6. Members of the league will do a draft before the season starts. For now, we will focus on the spring season and fleet racing only.

Ideally, league members will draft x number of team race teams, and y number fleet race sailors. For now, we will focus on fleet racing. League members will draft 3 coed skippers, 3 coed crews, 3 womens skippers, and 3 womens crews.

There will be 8 starting sailors, and the other 4 will be on the bench. Substitutions will only be allowed during the week, and after racing on Saturday but before midnight.

## Scoring Algorithms
### Fleet Racing
The score for each sailor on a given weekend will be based on the following inputs:
* Regatta level {A, B, C, other}
* Number of races sailed [0, # of teams]
* Number of teams entered [2, 18]
* Place in each race [1, # of teams]

Algorithm will be determined after league pool data is scraped and compiled from web.

Interesting links
* NEISA SCORING GUIDE - https://neisa.collegesailing.org/documents/NEISA_Performance_Ranking_System_Guide.pdf
* Techscore homepage - https://scores.collegesailing.org/

## Parsing and Reading Data
Each regatta page has a unique link name which will make full automation difficult. For example the Co-ed Showcase regatta has name "/coed-showcase/". The Captain Hurst has the name "/captain-hurst-bowl/", the Danmark Trophy is "/danmark/", etc.

Thinking we might have to input a schedule ahead of time, and guess the names of the regatta pages, or update them each week. Might be able to pull from icsa website.


