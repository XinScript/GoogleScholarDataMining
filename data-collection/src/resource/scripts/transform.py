arr = []
with open('IEEE_word_abbr.txt','r') as f:
	full = f.readline().strip()
	abbr = f.readline().strip()
	while(full):
		new_line = "\""+abbr+"\":"+"\""+full+"\","
		arr.append(new_line)
		full = f.readline().strip()
		abbr = f.readline().strip()
with open('IEEE_words_abbr.json','w') as f:
	for line in arr:
		f.write(line)