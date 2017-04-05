import MySQLdb
import sys
# import Sastrawi package
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()
# open a database connection
# be sure to change the host IP address, username, password and database name to match your own
connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "dictionary")
connection2 = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "nonbaku")
# prepare a cursor object using cursor() method
#cursor = connection.cursor ()
# execute the SQL query using execute() method.
#cursor.execute ("select word from dictionary")
# fetch all of the rows from the query
#data = cursor.fetchall ()
# print the rows

#for row in data :
#	i=i+1
#	print i
#	print row[0]
# close the cursor object
#cursor.close ()
# close the connection
#connection.close ()

sentence = "liburan telah berakhir  terima kasih danau toba untuk keindahan yg kmu beri sampai bertemu u"
finalSentence = ""
words = sentence.split()   
for word in words:
	
	cursor = connection.cursor ()
	cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' "% (word))
	data = cursor.fetchall()
	stemWord=""
	for row in data:
		if row[0]!=0:
			print word+"->ada"
			finalSentence = finalSentence + word + " "
		else:
			print word+"->ga ada"
			stemWord = stemmer.stem(word)
			#print stemWord
			cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' "% (stemWord))
			data2 = cursor.fetchall()
			for row2 in data2:
				if row2[0]!=0:
					print "setelah di stem jadi '" + stemWord + "' ada"
					finalSentence = finalSentence + word + " "
				else:
					cursorNonBaku = connection2.cursor()
					cursorNonBaku.execute("SELECT baku FROM katanonbaku WHERE nonbaku='%s' "% (word))
					dataNonBaku = cursorNonBaku.fetchall()
					for rowNonBaku in dataNonBaku:
						finalSentence = finalSentence + rowNonBaku[0] + " "

	cursor.close()
# exit the program

connection.close();
print "Before Convert Word: \n'" + sentence + "'"
print "After Convert Word: \n'" +finalSentence +"'"
sys.exit()