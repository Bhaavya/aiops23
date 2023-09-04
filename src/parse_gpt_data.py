'''
For parsing and formatting ChatGPT generated textual samples + labels
'''
# entities = ['Code Block','User Interface Element','File Name','Data Structure','Library','Sentence']
# emap = {'Code Block':'Code_Block','User Interface Element':'User_Interface_Element','File Name':'File_Name','Data Structure':'Data_Structure','Library':'Library'}

entities = ['Person','Organization','Location','Miscellaneous']
emap = {'Person':'PER','Organization':'ORG','Location':'LOC','Miscellaneous':'MISC'}

def main():
	with open(gpt_path) as f:
		data = f.read()
	out_sents = []
	out_labels = []
	for row in data.split('\n\n'):
		sents = row.split('\n')
		sent = sents[0]
		if sent.startswith('Sentence'):
			sent = sent.split(':')[1]
		olabels = ['O' for _ in range(len(sent.split()))]
		for extent in sents[1:]:
			for ent in entities:
				if extent.startswith(ent):
					content = extent.split(':')[1]
					sent_split = sent.lower().split()
					for w in content.split():
					
						try:
							idx = sent_split.index(w.lower())

						except:
							try:
								idx = sent_split.index(w.lower().strip(','))
							except:
								idx = -1
						if idx != -1:
							print(idx,olabels)
							olabels[idx] = 'B-'+emap[ent]

		prev = 'O'
		print(olabels)
		for idx,o in enumerate(olabels):

			cur = o
			
			if cur == prev and cur!='O':
				olabels[idx] = 'I-'+cur.split('B-')[1]

			prev = o
		out_sents.append(sent)
		out_labels.append(olabels)

	with open(opath,'w') as f:
		for idx1,ost in enumerate(out_sents):
			for idx2,w in enumerate(ost.split()):
				f.write(w+'\t'+out_labels[idx1][idx2]+'\n')
			f.write('\n')

if __name__ == '__main__':
	gpt_path = '../data/soner/gpt.txt'
	opath = '../data/soner/train_chat_conll.txt'
	main()