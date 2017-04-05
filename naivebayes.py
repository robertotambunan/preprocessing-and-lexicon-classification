import MySQLdb
import sys
from string import digits
import re

connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
cursor = connection.cursor()
connectionNB = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "naivebayes")
cursorNB = connectionNB.cursor()
cursor.execute("SELECT tweets FROM hasil WHERE skor= 1")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursorNB.execute("SELECT count(*) FROM doc_positif WHERE kata='%s' "% (splitter))
 		result=cursorNB.fetchone()
 		if result[0] == 0:
 			try:
				cursorNB.execute("""INSERT INTO doc_positif (kata, jumlah) VALUES (%s,%s)""",(splitter, '1'))
				connectionNB.commit()
			except TypeError as e:
				print(e)
				connectionNB.rollback()
				print "failed"
		else:
			cursorNB.execute("SELECT jumlah FROM doc_positif WHERE kata='%s' "% (splitter))
 			resultz=cursorNB.fetchone()
 			jumlah = int(resultz[0])+1
 			cursorNB.execute ("""UPDATE doc_positif SET jumlah=%s WHERE kata=%s """, (str(jumlah), splitter))


cursor.execute("SELECT tweets FROM hasil WHERE skor= 2")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursorNB.execute("SELECT count(*) FROM doc_negatif WHERE kata='%s' "% (splitter))
 		result=cursorNB.fetchone()
 		if result[0] == 0:
 			try:
				cursorNB.execute("""INSERT INTO doc_negatif (kata, jumlah) VALUES (%s,%s)""",(splitter, '1'))
				connectionNB.commit()
			except TypeError as e:
				print(e)
				connectionNB.rollback()
				print "failed"
		else:
			cursorNB.execute("SELECT jumlah FROM doc_negatif WHERE kata='%s' "% (splitter))
 			resultz=cursorNB.fetchone()
 			jumlah = int(resultz[0])+1
 			cursorNB.execute ("""UPDATE doc_negatif SET jumlah=%s WHERE kata=%s """, (str(jumlah), splitter))

cursor.execute("SELECT tweets FROM hasil WHERE skor= 0")
data = cursor.fetchall()

for row in data:
	sentence = row[0]
	sentenceArr = sentence.split()
	for splitter in sentenceArr:
		print splitter
		cursorNB.execute("SELECT count(*) FROM doc_netral WHERE kata='%s' "% (splitter))
 		result=cursorNB.fetchone()
 		if result[0] == 0:
 			try:
				cursorNB.execute("""INSERT INTO doc_netral (kata, jumlah) VALUES (%s,%s)""",(splitter, '1'))
				connectionNB.commit()
			except TypeError as e:
				print(e)
				connectionNB.rollback()
				print "failed"
		else:
			cursorNB.execute("SELECT jumlah FROM doc_netral WHERE kata='%s' "% (splitter))
 			resultz=cursorNB.fetchone()
 			jumlah = int(resultz[0])+1
 			cursorNB.execute ("""UPDATE doc_netral SET jumlah=%s WHERE kata=%s """, (str(jumlah), splitter))


cursorNB.close()
connectionNB.close()
cursor.close()
connection.close()