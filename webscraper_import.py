# Pyton script to take data from per_weekend.py and import to postgres database
# Using middleware psycopg

import psycopg2 as psy
import os
import urlparse


os.environ['DATABASE_URL'] = 'postgres://vqpyexosbmxcby:ff4fd82d930fe0bd04ee6e7fa21192f124d404c764b04032338b360b82ef79ab@ec2-174-129-27-3.compute-1.amazonaws.com:5432/deq4o4fdii9fl3'


#urlparse.uses_netloc.append("postgres")

DATABASE_URL = os.environ['DATABASE_URL']

url = urlparse.urlparse(os.environ['DATABASE_URL'])


con = psy.connect(
	database = url.path[1:],
	user = url.username,
	password = url.password,
	host = url.hostname,
	port = url.port,
	)



#cursor
cur = con.cursor()


create_table = "CREATE TABLE Thompson_Trophy(name VARCHAR(50) PRIMARY KEY, schoolref VARCHAR(50), regatta VARCHAR(50), div CHAR(1), r1 BIGINT, r2 BIGINT, r3 BIGINT, r4 BIGINT, r5 BIGINT, r6 BIGINT, r7 BIGINT, r8 BIGINT, r9 BIGINT, r10 BIGINT, r11 BIGINT, r12 BIGINT, fantasy_points BIGINT);"
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")



cur.execute(query_drop)


#commit changes
con.commit()

#close the cursor
cur.close()

#close the connection
con.close()