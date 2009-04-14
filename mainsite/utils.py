MONTHS_DICT = {'January':'Janeiro',
			   'February':'Fevereiro',
			   'March':u'Março',
			   'April':'Abril',
			   'May':'Maio',
			   'June':'Junho',
			   'July':'Julho',
			   'August':'Agosto',
			   'September':'Setembro',
			   'October':'Outubro',
			   'November':'Novembro',
			   'December':'Dezembro'}
			   
def translate(word):
	if word in MONTHS_DICT.keys(): return MONTHS_DICT[word]
	else: return word