# -*- coding: utf-8 -*-
import MySQLdb
import sys
from string import digits
import decimal
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def removeURL(tweet):
	p1 = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')
	tweet_url = re.sub(p1, '', tweet)
	return tweet_url;

def caseFolding(tweet):
	res = tweet.translate(None, digits)
	res = res.lower()
	return res

def removeUnimportantSymbol(tweet):
	symbols = [ '>:]',':-)',':)',':o)',':]' ,':3',':c)',':>','=]','8)','=)',':}',':^)', '>:D',':-D',':D','8-D','8D','x-D','xD','=-D','=D','=-3','=3', ':(', ':-('];
	temp_symbol =""
	for symbol in symbols:
		if symbol in tweet:
			temp_symbol += symbol+" "
	clean_tweet = re.sub(r'[^A-Za-z0-9 -]', ' ', tweet)
	clean_tweet = clean_tweet + temp_symbol
	return clean_tweet

def convertWord(sentence):
	f = open("KataBaru.txt","a+")
	symbols = [ '>:]',':-)',':)',':o)',':]' ,':3',':c)',':>','=]','8)','=)',':}',':^)', '>:D',':-D',':D','8-D','8D','x-D','xD','=-D','=D','=-3','=3', ':(', ':-('];
	temp_symbol =""
	for symbol in symbols:
		if symbol in sentence:
			temp_symbol += symbol+" "
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
	finalSentence = ""
	words = sentence.split()   
	for word in words:
		
		cursor = connection.cursor ()
		cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' "% (word))
		data = cursor.fetchall()
		stemWord=""
		for row in data:
			if row[0]!=0:
				#print word+"->ada"
				finalSentence = finalSentence + word + " "
			else:
				#print word+"->ga ada"
				stemWord = stemmer.stem(word)
				#print stemWord
				cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' "% (stemWord))
				data2 = cursor.fetchall()
				for row2 in data2:
					if row2[0]!=0:
						#print "setelah di stem jadi '" + stemWord + "' ada"
						finalSentence = finalSentence + word + " "
					else:
						cursor.execute("SELECT baku FROM katanonbaku WHERE nonbaku='%s' "% (word))
						dataNonBaku = cursor.fetchall()
						if not cursor.rowcount:
							f.write(word+"\n")
						for rowNonBaku in dataNonBaku:
							finalSentence = finalSentence + rowNonBaku[0] + " "

		cursor.close()
	connection.close()
	f.close()
	return finalSentence + " " + temp_symbol

def removeStopword(tweet):
	symbols = [ '>:]',':-)',':)',':o)',':]' ,':3',':c)',':>','=]','8)','=)',':}',':^)', '>:D',':-D',':D','8-D','8D','x-D','xD','=-D','=D','=-3','=3', ':(', ':-('];
	temp_symbol =""
	for symbol in symbols:
		if symbol in sentence:
			temp_symbol += symbol+" "
	connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
	words = tweet.split()
	tempWord = ""
	for word in words:
		cursor = connection.cursor ()
		cursor.execute("SELECT count(*) FROM dictionary WHERE word='%s' AND stopword='%s' "% (word,"Ya"))
		data = cursor.fetchall()
		for row in data:
			if row[0]==0:
				tempWord += word+" "
		cursor.close()
	return tempWord + " " + temp_symbol


def stemming(tweet):
	symbols = [ '>:]',':-)',':)',':o)',':]' ,':3',':c)',':>','=]','8)','=)',':}',':^)', '>:D',':-D',':D','8-D','8D','x-D','xD','=-D','=D','=-3','=3', ':(', ':-('];
	temp_symbol =""
	for symbol in symbols:
		if symbol in sentence:
			temp_symbol += symbol+" "
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()	
	output  = stemmer.stem(tweet)
	return output + " " + temp_symbol





connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
cursor = connection.cursor()
cursor.execute("SELECT tweets, id_tweetmentah FROM tweetmentah")
data = cursor.fetchall()
count = 0

#Jumlah seluruh kata yang positif
cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE  kategori='%s'"% ('1'))
sumPositif = cursor.fetchone()[0]

#Jumlah seluruh kata yang negatif
cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE  kategori='%s'"% ('-1'))
sumNegatif = cursor.fetchone()[0]

#Jumlah seluruh kata yang netral
cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE  kategori='%s'"% ('0'))
sumNetral = cursor.fetchone()[0]


#Kosakata yang ada pada semua kategori
cursor.execute("SELECT count(distinct kata) FROM doc_pembelajaran")
kosakata = cursor.fetchone()[0]



for row in data:
	if count >= 8000:
		idTweet = row[1]
		sentence = row [0]
		removeUrlResult = removeURL(sentence)
		caseFoldingResult = caseFolding(removeUrlResult)
		removeUnimportantSymbolResult = removeUnimportantSymbol(caseFoldingResult)
		convertWordResult = convertWord(removeUnimportantSymbolResult)
		removeStopwordResult = removeStopword(convertWordResult)
		stemmingResult = stemming(removeStopwordResult)
		
		#Menginisiasi variabel yang akan menyimpan nilai vmap. Jika nantinya tidak ada kata yang lolos dari semua preprocessing (tweet hasil preprocessing ialah null),
		#Maka vmap akan diberikan value 0, jika tweet hasil preprocessing tidak berisi null, maka inisisasi pertama vmap ialah 1 untuk operasi perkalians
		if stemmingResult=="":
			VMapPositif = 0
			VMapNegatif = 0
			VMapNetral = 0
		else:
			VMapPositif = 1
			VMapNegatif = 1
			VMapNetral = 1

		splitWord = stemmingResult.split()
		#print count-7999
		#print stemmingResult
		


		for rowSplitWord in splitWord:
			#Ambil jumlah kata  yang sedang di foreach di bagian positif
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('1',rowSplitWord))
			nkPositifGetData = cursor.fetchone()
			#Menyimpan jumlah kata positif tertentu kedalam variabel
			if nkPositifGetData:
				nkPositif = nkPositifGetData[0]
			else:
				nkPositif = 0
			

			#Ambil jumlah kata  yang sedang di foreach di bagian negatif
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('-1',rowSplitWord))
			nkNegatifGetData = cursor.fetchone()
			#Menyimpan jumlah kata negatif tertentu kedalam variabel
			if nkNegatifGetData:
				nkNegatif = nkNegatifGetData[0]
			else:
				nkNegatif = 0 

			
			#Ambil jumlah kata  yang sedang di foreach di bagian netral
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('0',rowSplitWord))
			nkNetralGetData = cursor.fetchone()
			#Menyimpan jumlah kata negatif tertentu kedalam variabel
			if nkNetralGetData:
				nkNetral = nkNetralGetData[0]
			else:
				nkNetral = 0




			#print rowSplitWord
			#print "NK Positif = ", nkPositif
			#print "NK Negatif = ", nkNegatif
			#print "NK Netral = ", nkNetral
			#Menghitung vmap per kata untuk positif
			perhitunganPositif = (nkPositif+1)/float(sumPositif+kosakata)

			#Menghitung vmap per kata untuk netral
			perhitunganNetral = (nkNetral+1)/float(sumNetral+kosakata)

			#Menghitung vmap per kata untuk negatif
			perhitunganNegatif = (nkNegatif+1)/float(sumNegatif+kosakata)			
			
			#Melakukan perkalian vmap positif
			VMapPositif *= perhitunganPositif

			#Melakukan perkalian vmap negatif
			VMapNegatif *= perhitunganNegatif

			#Melakukan perkalian vmap netral
			VMapNetral *= perhitunganNetral


		#mengalikan vmap positif dengan 0,33 (Karena terdapat tiga kategori, peluang => (1/3 = 0,33))
		VMapPositif *= 0.33

		#mengalikan vmap negatif dengan 0,33 (Karena terdapat tiga kategori, peluang => (1/3 = 0,33))
		VMapNegatif *= 0.33

		#mengalikan vmap netral dengan 0,33 (Karena terdapat tiga kategori, peluang => (1/3 = 0,33))
		VMapNetral *= 0.33

		#Memberikan nilai default untuk skor
		hasil = "netral"

		#Memberikan hasil akhir dari sebuah tweet
		if VMapPositif > VMapNegatif and VMapPositif > VMapNetral:
			hasil = "positif"
			print count-7999
			print "Tweet : " , sentence
			print stemmingResult
			print "Vmap Positif :",VMapPositif
			print "Vmap Negatif :",VMapNegatif
			print "Vmap Netral :",VMapNetral

			print hasil
			print ""
		if VMapNegatif > VMapPositif and VMapNegatif > VMapNetral:
			hasil = "negatif"
			
		if VMapNetral > VMapPositif and VMapNetral > VMapNegatif:
			hasil = "netral"

		#print "Vmap Positif :",VMapPositif
		#print "Vmap Negatif :",VMapNegatif
		#print "Vmap Netral :",VMapNetral

		#print hasil
		#print ""

	count += 1

cursor.close()
connection.close()