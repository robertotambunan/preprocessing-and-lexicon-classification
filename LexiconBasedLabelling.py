# -*- coding: utf-8 -*-
import MySQLdb
import sys
from string import digits
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

	finalSentence = ""
	words = sentence.split()   
	for word in words:
		connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
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

#Just for Saving word in txt for reviewing
f1 = open("LexiconPositif.txt","a+")
f2 = open("LexiconNegatif.txt","a+")
f3 = open("LexiconNetral.txt","a+")

#Main Driver
connection = MySQLdb.connect (host = "127.0.0.1", user = "root", passwd = "", db = "opinionmining")
cursor = connection.cursor()


cursor.execute("SELECT tweets, id_tweetmentah FROM tweetmentah")
dataFinal = cursor.fetchall()
count = 0
positifLblCnt = 0;
negatitifLblCnt = 0;
netralLblCnt = 0;
for rowFinal in dataFinal:
	if count==11311:
		break
	count += 1
	print ""
	print count
	sentence = rowFinal[0]
	idTweet = rowFinal[1]
	print "Tweet:\n"+sentence
	#Remove URL
#	print "Hasil Remove URL:"
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
#	print stemmingResult+"\n\n"
	#Final Preprocessing
	print "Final Result"
	print stemmingResult
	splitResult = stemmingResult.split()
	splitResultLength = len(splitResult)
	positif = 0
	negatif = 0
	idx=0
	#Ini untuk lexiconnya.
	for splitter in splitResult:
		cursor.execute("SELECT sentiment FROM dictionary WHERE word='%s' "% (splitter))
		dataKamus = cursor.fetchall()
		for rowKamus in dataKamus:
			if rowKamus[0]=='positif':
				positif+=1
				if idx>0:
					#untuk negasi positif
					if(splitResult[idx-1]=='tidak' or splitResult[idx-1]=='belum' or splitResult[idx-1]=='saber' or splitResult[idx-1]=='tak' or splitResult[idx-1]=='jangan' or splitResult[idx-1]=='bukan' or splitResult[idx-1]=='hapus' or splitResult[idx-1]=='belum' or  splitResult[idx-1]=='antisipasi'):
						positif-=1
						#negatif+=1
			if rowKamus[0]=='negatif':
				negatif+=1
				if idx>0:
					#untuk negasi negatif
					if(splitResult[idx-1]=='tidak' or splitResult[idx-1]=='belum' or splitResult[idx-1]=='saber' or splitResult[idx-1]=='tak' or splitResult[idx-1]=='jangan' or splitResult[idx-1]=='bukan' or splitResult[idx-1]=='hapus' or splitResult[idx-1]=='belum' or  splitResult[idx-1]=='antisipasi'):
						positif+=1
						negatif-=1
		#untuk kata-kata pengecualian
		if splitResult[idx]==":(":
			negatif+=1
		if splitResult[idx]==":)":
			positif+=1
		if idx>0:
			if splitResult[idx]=='biasa' and splitResult[idx-1]=='luar':
				positif+=1
				splitResultLength-=1
			if splitResult[idx]=='mati' and splitResult[idx-1]=='setengah':
				negatif-=1
				splitResultLength-=1
			if splitResult[idx]=='royong' and splitResult[idx-1]=='gotong':
				positif+=2
				splitResultLength-=1
			if splitResult[idx]=='warna' and splitResult[idx-1]=='penuh':
				positif+=1
				splitResultLength-=1
			if splitResult[idx]=='rute' and splitResult[idx-1]=='buka':
				positif+=1
				splitResultLength-=1
			if splitResult[idx]=='kelas' and splitResult[idx-1]=='naik':
				positif+=1
				splitResultLength-=1
		
		idx+=1

	
	#Menghitung
	if float(splitResultLength)>0:
		scorePositif = positif/float(splitResultLength)
		scoreNegatif = negatif/float(splitResultLength)
		scoreTotal = scorePositif - scoreNegatif
	else:
		scoreTotal = 0
	skors = '0';
	if scoreTotal >= 0.2:
		print "Positif"
		skors ='1'
		positifLblCnt+=1
		f1.write("No :"+ str(positifLblCnt) + "\nTweet : "+ sentence +"\nPreprocessing: "+ stemmingResult+"\nNilai: "+ str(scoreTotal)+ "\nKlasifikasi : Positif\n\n")
	elif scoreTotal <= -0.2:
		print "Negatif"
		skors ='-1'
		negatitifLblCnt+=1
		f2.write("No :"+ str(negatitifLblCnt) +"\nTweet : "+ sentence +"\nPreprocessing: "+ stemmingResult+"\nNilai: "+ str(scoreTotal)+ "\nKlasifikasi : Negatif\n\n")
	else:
		print "Neutral"
		skors ='0'
		netralLblCnt+=1
		f3.write("No :"+ str(netralLblCnt) +"\nTweet : "+ sentence +"\nPreprocessing: "+ stemmingResult+"\nNilai: "+ str(scoreTotal)+ "\nKlasifikasi : Netral\n\n")
	print scoreTotal
	print "Positif: " , positif;
	print "Negatif: " , negatif;
	print "Score Positif-Negatif ", scorePositif , " ", scoreNegatif, "\n"
	#print int(idTweet),stemmingResult,int(skors)
	#try:
	#	cursor.execute("""INSERT INTO hasil (id_tweetmentah, tweets, skor) VALUES (%s,%s,%s)""",(str(idTweet),stemmingResult,str(skors)))
	#	connection.commit()
	#except TypeError as e:
	#	print(e)
	#	connection.rollback()
	#	print "failed"
print "Positif Label = ", positifLblCnt
print "Negatif Label = ", negatitifLblCnt
print "Netral Label  = ", netralLblCnt		
f1.close()
f2.close()
f3.close()
cursor.close()
connection.close()