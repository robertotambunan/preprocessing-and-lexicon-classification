import re
tweet = 'liburan telah berakhir =] terima kasih danau toba untuk keindahan yang kau beri sampai bertemu \u :)]'

symbols = [ '>:]',':-)',':)',':o)',':]' ,':3',':c)',':>','=]','8)','=)',':}',':^)', '>:D',':-D',':D','8-D','8D','x-D','xD','=-D','=D','=-3','=3'];
temp_symbol =""
for symbol in symbols:
	if symbol in tweet:
		temp_symbol += symbol+" "

print temp_symbol
print 'before:'
print tweet
clean_tweet = re.sub(r'[^A-Za-z0-9 -]', '', tweet)
print clean_tweet + temp_symbol