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
	f = open("KataBaru1.txt","a+")
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
	if output == "riah":
		output = meriah
	return output + " " + temp_symbol





connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
cursor = connection.cursor()
cursor.execute("SELECT tweets, id_tweetmentah FROM tweetmentah")
data = cursor.fetchall()
count = 0
for row in data:
	if count >=8000 and count < 10000:
		idTweet = row[1]
		sentence = row[0]
		removeUrlResult = removeURL(sentence)
	#	print removeUrlResult +"\n\n"
		#Case Folding
	#	print "Hasil Case Folding:"
		caseFoldingResult = caseFolding(removeUrlResult)
	#	print caseFoldingResult+"\n\n"
		#Remove Unimportant Symbol
	#	print "Hasil Remove Unimportant Symbol:"
		removeUnimportantSymbolResult = removeUnimportantSymbol(caseFoldingResult)
	#	print removeUnimportantSymbolResult+"\n\n"
		#Convert Word
	#	print "Hasil Convert Word:"
		convertWordResult = convertWord(removeUnimportantSymbolResult)
	#	print convertWordResult+"\n\n"
		#Remove Stopword
	#	print "Hasil Remove Stopword"
		removeStopwordResult = removeStopword(convertWordResult)
	#	print removeStopwordResult+"\n\n"
		#Stemming
	#	print "Hasil Stemming"
		stemmingResult = stemming(removeStopwordResult)
		splitWord = stemmingResult.split()
		if stemmingResult=="":
			NBMultiplyPos = 0
			NBMultiplyNeg = 0
			NBMultiplyNet = 0
		else:
			NBMultiplyPos = 1
			NBMultiplyNeg = 1
			NBMultiplyNet = 1
		print " "
		print count-7999
		print "Tweet:\n" + sentence
		print "Preprocessing:\n"+stemmingResult
		cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE  kategori='%s'"% ('1'))
		sumPositif = cursor.fetchone()[0]
		cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE  kategori='%s'"% ('-1'))
		sumNegatif = cursor.fetchone()[0]
		cursor.execute("SELECT SUM(jumlah) FROM doc_pembelajaran WHERE kategori='%s'"% ('0'))
		sumNetral = cursor.fetchone()[0]				
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s'"% ('1'))
		cntPositif = cursor.fetchone()[0]
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s'"% ('-1'))
		cntNegatif = cursor.fetchone()[0]
		cursor.execute("SELECT count(*) FROM doc_pembelajaran WHERE kategori='%s'"% ('0'))
		cntNetral = cursor.fetchone()[0]
		for splitter in splitWord:
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('1',splitter))
			crsKataPos = cursor.fetchone()
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('-1',splitter))
			crsKataNeg = cursor.fetchone()
			cursor.execute("SELECT jumlah FROM doc_pembelajaran WHERE kategori='%s' AND kata='%s' "% ('0',splitter))
			crsKataNet = cursor.fetchone()
			if crsKataPos:
				cntKataPos = crsKataPos[0]
			else:
				cntKataPos = 0
			if crsKataNeg:
				cntKataNeg = crsKataNeg[0]
			else:
				cntKataNeg = 0
			if crsKataNet:
				cntKataNet = crsKataNet[0]
			else:
				cntKataNet = 0

			posCalc = ((cntKataPos+1)/(sumPositif+cntPositif)) * decimal.Decimal(0.333)
			negCalc = ((cntKataNeg+1)/(sumNegatif+cntNegatif)) * decimal.Decimal(0.333)
			netCalc = ((cntKataNet+1)/(sumNetral+cntNetral)) * decimal.Decimal(0.333)
			NBMultiplyPos*=posCalc
			NBMultiplyNeg*=negCalc
			NBMultiplyNet*=netCalc
			posCalc = 0
			negCalc = 0
			netCalc = 0
		skoring = 0;
		print "Positif Score: " , NBMultiplyPos
		print "Negatif Score: " ,NBMultiplyNeg
		print "Netral Score: " ,NBMultiplyNet
		if NBMultiplyPos>NBMultiplyNeg and NBMultiplyPos>NBMultiplyNet:
			print "positif"
			skoring = 1
		elif NBMultiplyNeg>NBMultiplyPos and NBMultiplyNeg>NBMultiplyNet:
			print "negatif"
			skoring = -1
		else:
			print "netral"
			skoring = 0

		try:
			cursor.execute("""INSERT INTO hasil_nb (id_tweetmentah, tweets, skor) VALUES (%s,%s,%s)""",(str(idTweet),stemmingResult,str(skoring)))
			connection.commit()
		except TypeError as e:
			print(e)
			connection.rollback()
			print "failed"
	count +=1


cursor.close()
connection.close()