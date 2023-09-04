import json 
import openai 
import time
def read_f(path):
	with open(path) as f:
		data = f.read()
	sents = []
	labels = []
	print(path)
	for l in data.split('\n\n'):
		sent = []
		label = []
		for w in l.split('\n'):
			# if len(w.strip().split())>1:
			if len(w.strip().split('\t'))>1:
				sent.append(w.strip().split('\t')[0])
				label.append(w.strip().split('\t')[1])
		if len(sent) > 0:
			sents.append(' '.join(sent))
			labels.append(label)

	return sents,labels

def query_gpt(sent):
	# print("Extract Code Block, User Interface Element, File Name, Data Structure, and Library entities from the following sentences.\nUse the following format:\nCode Block:\nUser Interface Element:\nFile Name:\nData Structure:\nLibrary:\nWrite NA for the entities not present in the sentence.\n\n Sentence: {}\n".format(sent))
	practice_sent1 = "I am adding the Toolbar from appcompat and have created the menu xml file."
	practice_resp1 = '''
	User Interface Element: Toolbar
	File Name: menu xml
	Library: appcompat
	'''
	practice_sent2 = "Given an array, I need to find the indices of the nearest non-coprime number ( i.e. GCD(Ai, Aj) > 1, for any Ai and Aj in the array"
	practice_resp2 = '''
	Data Structure: array
	Code Block: GCD(Ai, Aj) > 1, for any Ai and Aj in the array
	'''

	practice_sent3 = "Take your message header as-is, e.g. a List or Collection and send to each destination."
	practice_resp3 = '''
	User Interface Element: header
	Data Structure: List
	Library: Collection
	'''

	response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user","content":"Extract Code Block , User Interface Element, File Name, Data Structure, and Library entities from the following sentences.\nUse the following format:\nCode Block:\nUser Interface Element:\nFile Name:\nData Structure:\nLibrary :\nWrite NA for the entities not present in the sentence.\n\n Sentence: {}\n".format(practice_sent1)},
        {"role": "assistant","content":practice_resp1},

        {"role":"user","content":"Sentence: {}\n".format(practice_sent2)},
        {"role": "assistant","content":practice_resp2},

        {"role":"user","content":"Sentence: {}\n".format(practice_sent3)},
        {"role": "assistant","content":practice_resp3},

        {"role":"user","content":"Sentence: {}\n".format(sent)},
        # {"role": "user","content":"Extract Person, Organization, Location, and Miscellaneous entities from the following sentences.\nUse the following format:\nPerson:\nOrganization:\nLocation:\nMiscellaneous:\nWrite NA for the entities not present in the sentence.\n\n Sentence: {}\n".format(sent)}
    ]
)
	print(response['choices'][0]['message']['content'])
	return response['choices'][0]['message']['content']


def main():
  sents, inlabels = read_f(path)
  out_dict = {'sents':sents,'inlabels':inlabels,'outlabels':[]}
  # with open(opath) as f:
  # 	out_dict = json.load(f)
  outlabels = []
  for idx,sent in enumerate(sents[0:]):
  	print(idx)
  	time.sleep(0.15)
  	resp = query_gpt(sent)

  	out_dict['outlabels'].append(resp)
  	with open(opath,'w') as f:
  		json.dump(out_dict,f)
  
  

if __name__ == '__main__':
  openai.api_key = API_KEY
  path = '../data/soner/test.txt'
  opath = '../data/soner/chatgpt.json'
  main()
