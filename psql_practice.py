import sys
import psycopg2 as psy
import os

import per_weekend

# included in .GITIGNORE


# determines if a table with name 'regatta_name' exists in the database
# parameters: regatta name (also the table name), active connection to a database
# returns: boolean
def table_exists(regatta_name, con):	
	cur = con.cursor()
	cur.execute("SELECT exists(SELECT * FROM information_schema.tables WHERE table_name=%s)", (regatta_name,))
	exists_bool = cur.fetchone()[0]

	cur.close()
	return exists_bool



# creates an empty table with 18 race columns and name as regatta_name
# params: regatta name, active connection to database
def create_regatta_table(regatta_name, con):
	cur = con.cursor()

	create_table = '''CREATE TABLE {}(id BIGSERIAL PRIMARY KEY,
					 name VARCHAR(64) , schoolref VARCHAR(64), regatta VARCHAR(32),
					  div CHAR(1), r1 BIGINT, r2 BIGINT, r3 BIGINT, r4 BIGINT, 
					  r5 BIGINT, r6 BIGINT, r7 BIGINT, r8 BIGINT, r9 BIGINT, 
					  r10 BIGINT, r11 BIGINT, r12 BIGINT, r13 BIGINT, r14 BIGINT,
					  r15 BIGINT, r16 BIGINT, r17 BIGINT, r18 BIGINT
					  );'''.format(regatta_name)

	cur.execute(create_table)
	con.commit()
	cur.close()
	return


'''
does not work - can't figure out a way to dynamically update a table
for example, if only 3 races have been complete, how do you only update 3 race columns in the table

Maybe use UPDATE instead of INSERT?
'''
def populate_empty_regatta_table(regatta_name, con, regatta_data):
	num_race_cols = len(regatta_data[1]) - 4

	str_format = num_race_cols * '%s,' + ')'

	cur = con.cursor()

	populate_query = "INSERT INTO {} VALUES(DEFAULT,".format(regatta_name) + str_format + ', row)'

	print(populate_query)
	for row in regatta_data[1:]:
		cur.execute(populate_query)

	con.commit()
	cur.close()


def main(regatta_name):
	sailors_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'sailors')
	scores_url = 'https://scores.collegesailing.org/s18/{}/{}/'.format(regatta_name, 'full-scores')
	regatta_data = per_weekend.regatta_matrix(scores_url, sailors_url)

	con = psy.connect(
		database = "test",
		host = "localhost",
		port = "5432",
		)

	#cursor
	cur = con.cursor()

	#if not table_exists(regatta_name, con):
		# create_regatta_table()

	#cur.execute("CREATE TABLE {}(id BIGSERIAL PRIMARY KEY, name VARCHAR(64) NOT NULL, div CHAR(1) NOT NULL, r1 BIGINT, r2 BIGINT);".format('test'))

	#cur.execute("INSERT INTO test VALUES(DEFAULT, %s, %s)", ('Carl', 'B'))

	create_regatta_table(regatta_name, con)

	populate_empty_regatta_table(regatta_name, con, regatta_data)

	# else:

	# if table doesn't exist
		# create table - need to do these things to create table
			# check the number of columns in the 2d array given by thompson_data
			# create a table with this number of columns
			# add the data

	# if table exists - add to table
		# check number of columns in 2d array given by thompson data
		# if num of columns == num of columns in table -> do nothing
		# else if num of columns > num colums in table 
		# else (num of colums < num cols in table) -> throw error





	# cur.execute(query_drop)


	#commit changes
	con.commit()

	#close the cursor
	cur.close()

	#close the connection
	con.close()




if __name__ == '__main__':
	main('thompson')