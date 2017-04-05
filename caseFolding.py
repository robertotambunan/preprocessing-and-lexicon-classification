from string import digits
print 'before:'
s = 'Liburan telah berakhir, terima kasih danau toba untuk keindahan yang kau beri, sampai bertemu \u2026 '
print s
res = s.translate(None, digits)
res = res.lower()
print 'after:'
print res