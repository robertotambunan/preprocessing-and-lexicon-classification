import MySQLdb
import sys

# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "dictionary")
sentence = "liburan telah berakhir  terima kasih danau toba untuk keindahan yang kau beri sampai bertemu u"
words = sentence.split()
temp=""   
for word in words:
	cursor = connection.cursor ()
	cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' AND stopword='%s' "% (word,"Ya"))
	data = cursor.fetchall()
	for row in data:
		if row[0]==0:
			temp += word+" "
		
	cursor.close()
# exit the program
print temp
connection.close()
sys.exit()