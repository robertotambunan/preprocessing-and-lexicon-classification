# -*- coding: utf-8 -*-
import re
print 'before:'
tweet = 'Liburan telah berakhir, terima kasih danau toba untuk keindahan yang kau beri, sampai bertemu \u2026 https://t.co/39mozV9Y97'
print tweet
p1 = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')


tweet_clean = re.sub(p1, '', tweet)
print 'after:'
print tweet_clean