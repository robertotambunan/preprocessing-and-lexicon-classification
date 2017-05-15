import MySQLdb
import sys
from string import digits
import re

connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining3000")
cursor = connection.cursor()

cursor.execute("SELECT tweets FROM hasil WHERE skor= 1")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('1',splitter))
 		result=cursor.fetchone()
 		if result[0] == 0:
 			try:
				cursor.execute("""INSERT INTO doc_pembelajaran (kata, jumlah, kategori) VALUES (%s,%s,%s)""",(splitter, '1','1'))
				connection.commit()
			except TypeError as e:
				print(e)
				connection.rollback()
				print "failed"
		else:
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('1',splitter))
 			resultz=cursor.fetchone()
 			jumlah = int(resultz[0])+1
 			cursor.execute ("""UPDATE doc_pembelajaran SET jumlah=%s WHERE kategori=%s and kata=%s """, (str(jumlah),'1',splitter))


cursor.execute("SELECT tweets FROM hasil WHERE skor= -1")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('-1',splitter))
 		result=cursor.fetchone()
 		if result[0] == 0:
 			try:
				cursor.execute("""INSERT INTO doc_pembelajaran (kata, jumlah, kategori) VALUES (%s,%s,%s)""",(splitter, '1','-1'))
				connection.commit()
			except TypeError as e:
				print(e)
				connection.rollback()
				print "failed"
		else:
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('-1',splitter))
 			resultz=cursor.fetchone()
 			jumlah = int(resultz[0])+1
 			cursor.execute ("""UPDATE doc_pembelajaran SET jumlah=%s WHERE kategori=%s and kata=%s """, (str(jumlah),'-1' ,splitter))

cursor.execute("SELECT tweets FROM hasil WHERE skor= 0")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('0',splitter))
 		result=cursor.fetchone()
 		if result[0] == 0:
 			try:
				cursor.execute("""INSERT INTO doc_pembelajaran (kata, jumlah, kategori) VALUES (%s,%s,%s)""",(splitter, '1','0'))
				connection.commit()
			except TypeError as e:
				print(e)
				connection.rollback()
				print "failed"
		else:
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' and kata='%s' "% ('0',splitter))
 			resultz=cursor.fetchone()
 			jumlah = int(resultz[0])+1
 			cursor.execute ("""UPDATE doc_pembelajaran SET jumlah=%s WHERE kategori=%s and kata=%s """, (str(jumlah),'0',splitter))



cursor.close()
connection.close()