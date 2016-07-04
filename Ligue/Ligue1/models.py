#~ from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
#~ from sklearn.naive_bayes import MultinomialNB
import csv
import re, unicodedata
from django.db import models
import os
import urllib.request, time
import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream, OAuthHandler, api

#######Le foot#######

#Classe equipe
CSV_FOLDER=os.path.dirname(__file__)
class Team() :
	def __init__(self,path,pattern,liste_surnoms,label) :
		path=path.split('/')[1]
		self.path=CSV_FOLDER+"\\Ligue1\\"+path+"\\"
		self.pattern=pattern
		self.liste_surnoms=liste_surnoms
		self.label=label
	def tweet_ref(self,r):
		p=""
		if r=='v':
			p=self.path+"tweet_vic.csv"
		elif r=='d' :
			p=self.path+"tweet_def.csv"
		else :
			p=self.path+"tweet_test.csv"
		return p
	def add_tweet(self,row) :
		p=self.tweet_ref('t')
		fd=open(p,'a+')
		fd.write(row)
		fd.write("\n")
		fd.close()
	def access_csv(self,categ):
		if categ=='victoire' :
			p=self.tweet_ref('v')
		if categ=='defaite' :
			p=self.tweet_ref('v')
		else :
			p=self.tweet_ref(categ)
		print(p)
		csvfile=open(p,"r") 
		sheet=csv.reader(csvfile,delimiter='~')
		
		return sheet
			#apres on peut faire for row in sheet
	def csv_to_data_ref(self) :
		L=['defaite','victoire']
		self.index=[]
		list=[]
		nb_def=0
		nb_vic=0
		for n in L :
			print(n)
			sheet=self.access_csv(n)
			for l in sheet:
				if l!=[]  :
					list+=[l[0]]
					if n=="defaite" :
						self.index+=[0]
						nb_def+=1
					elif n=="victoire" :
						self.index+=[1]
						nb_vic+=1
		if nb_def<3 :
			print('Pas de tweet defaite')
			return []
		elif nb_vic<3 :
			print('Pas de tweet victoire')
			return []
		return list
	def csv_to_data_test(self) :
		sheet=self.access_csv('test')
		listest=[]
		for l in sheet:
			if l!=[] :
				listest+=[l[0]]
		if len(listest)<3 :
			print('Pas assez de tweets a tester')
		return listest
	def data_to_classif_Bayes(self) :
		#~ print('debut classif')
		#~ count_vect = CountVectorizer()
		#~ print('ok')
		#~ data_ref=self.csv_to_data_ref()
		#~ print('ok')
		#~ self.cote={'defaite' : 0 , 'victoire' : 0}
		#~ if len(data_ref)<3:
			#~ print('Pas de tweet defaite ou victoire')
			#~ return self.cote
		#~ print('ok data ref')
		#~ X_train_counts = count_vect.fit_transform(data_ref)
		#~ nb_tot=X_train_counts.shape[0]
		#~ tfidf_transformer = TfidfTransformer()
		#~ X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
		#~ index=self.index
		#~ print(X_train_counts.shape, len(index))
		#~ self.clf = MultinomialNB().fit(X_train_tfidf,index)
		#~ L=['defaite','victoire']
		#~ print('ok')
		#~ docs_new=self.csv_to_data_test()
		#~ X_new_counts = count_vect.transform(docs_new)
		#~ X_new_tfidf = tfidf_transformer.transform(X_new_counts)
		#~ predicted = self.clf.predict(X_new_tfidf)
		#~ nb_vic=0
		#~ for doc, category in zip(docs_new, predicted):
			#~ if L[category]=="victoire" :
				#~ nb_vic+=1
		self.vic=10
		self.defa=5
		#~ try:
			#~ cote_def=1+nb_vic/(nb_tot-nb_vic)
		#~ except ZeroDivisionError:
			#~ cote_def=0
		#~ try:
			#~ cote_vic=1+(nb_tot-nb_vic)/nb_vic
		#~ except ZeroDivisionError:
			#~ cote_vic=0
		#~ self.cote['defaite']=cote_def
		#~ self.cote['victoire']=cote_vic
		#~ self.nb=[self.defa,self.vic]
		self.cote['defaite']=1
		self.cote['victoire']=3
		self.nb=[self.defa,self.vic]
		return self.nb


#Liste equipes

ASM=Team("Ligue1/ASM/",re.compile(r'monaco|@asm|#asm',re.IGNORECASE),["as_monaco","asmfc",'as monaco'],"Monaco")
ASSE=Team("Ligue1/ASSE/",re.compile(r'saint[\s-]?etienne|ASSE',re.IGNORECASE),["as saint etienne","#asSE","@asse"],"Saint-Etienne")
Bastia=Team("Ligue1/Bastia/",re.compile(r'bastia|SCB',re.IGNORECASE),["sporting club de bastia", "spirituturchinu", "s_c_bastia"],"Bastia")
Bordeaux=Team("Ligue1/Bordeaux/",re.compile(r'girondins|FCGB|ganalyse|bordeaux',re.IGNORECASE),["girondins","FCGB","ganalyse"],"Bordeaux")
Caen=Team("Ligue1/Caen/",re.compile(r'malherbe|caen|smc',re.IGNORECASE),["SMcaen","ff_smc"],"Caen")
EAG=Team("Ligue1/EAG/",re.compile(r'guingamp|EAG',re.IGNORECASE),["ea-guingamp","eag"],"Guingamp")
ETG=Team("Ligue1/ETG/",re.compile(r'evian|ETG',re.IGNORECASE),["etg","evian thonon"],"Evian-Thonon")
Lille=Team("Ligue1/Lille/",re.compile(r'lille|LOSC',re.IGNORECASE),["lilleosc","lille_osc","losc"],"Lille")
Lens=Team("Ligue1/Lens/",re.compile(r'Lens|rcl',re.IGNORECASE),["rc_lens","rclens","lensois"],"Lens")
Lorient=Team("Ligue1/Lorient/",re.compile(r'lorient|FCL',re.IGNORECASE),["fclorient","fc_lorient", "actusfcl","mercato_fcl","kopsudfcl"],"Lorient")
Lyon=Team("Ligue1/Lyon/",re.compile(r'lyon|[#@]OL',re.IGNORECASE),["@ol", "#OL","stadeol","olfeminin","olang","jm_aulas"],"Lyon")
Metz=Team("Ligue1/Metz/",re.compile(r'FCM|Metz',re.IGNORECASE),["fcmetz", "FC metz"],"Metz")
Montpellier=Team("Ligue1/Montpellier/",re.compile(r'montpellier|MHSC',re.IGNORECASE),["@mhsc","#mhsc"],"Montpellier")
Nantes=Team("Ligue1/Nantes/",re.compile(r'nantes|FCN',re.IGNORECASE),["fcnantes", "FC_Nantes", "fcn_business"],"Nantes")
Nice=Team("Ligue1/Nice/",re.compile(r'nice|OGCN',re.IGNORECASE),["OGC Nice","OGCN"],"Nice")
OM=Team("Ligue1/OM/",re.compile(r'marseille|\#om|\@om|teamom',re.IGNORECASE),["@om_","#om",'teamom','iamarseille'],"Marseille")
PSG=Team("Ligue1/PSG/",re.compile(r'paris-saint-germain|psg',re.IGNORECASE),["#psg","@psg","ff_psg"],"Paris")
Reims=Team("Ligue1/Reims/",re.compile(r'reims|sdr',re.IGNORECASE),["stade2reims","stadedereims","stade_de_reims","sdrofficielle"],"Reims")
Rennes=Team("Ligue1/Rennes/",re.compile(r'rennais|rennes|SRFC',re.IGNORECASE),["staderennais","srfc"],"Rennes")
TFC=Team("Ligue1/TFC/",re.compile(r'toulouse|TFC',re.IGNORECASE),["toulouse fc","tfc"],"Toulouse")
Ligue1=[ASM,ASSE,Bastia,Bordeaux,Caen,EAG,ETG,Lille,Lens,Lorient,Lyon,Metz,Montpellier,Nantes,Nice,OM,PSG,Reims,Rennes,TFC]


#print(PSG.data_to_classif_Bayes())
#Les matchs a venir, webscrapping
def liste_des_match() :
	team_liste=[]
	#Lien pour le calendrier de la ligue 1
	link='http://www.sports.fr/football/ligue-1/calendrier.html'
	print("recuperation liste des matchs")
	try :
		response = urllib.request.urlopen(link)
		html = response.read()
		html=str(html).split("suivant")[0]
		num_jour=time.localtime().tm_mday
		num_mois=time.localtime().tm_mon
		M=[]
		for i in range(0,6):
			j=num_jour+i
			if j<10 :
				if num_mois<10 :
					date_str='0'+str(num_jour)+'/0'+str(num_mois)
				else :
					date_str='0'+str(num_jour)+'/'+str(num_mois)
			elif j<32 :
				if num_mois<10 :
					date_str=str(j)+'/0'+str(num_mois)
				else :
					date_str=str(j)+'/'+str(num_mois)
			date_str=date_str+"/15"
			if re.search(date_str,html):
				date=html.split(date_str)
				#heure=date[1].split("class=\"utc\">")[1].split("<")[0]
				n=len(date)
				#print("le  ",date_str,"  on verra  ",n-1,"  matchs")
				for k in range(1,n) :
					match=date[k].split("Stats")[0]
					for team in Ligue1 :	
						if re.search(team.pattern,match) and team not in team_liste:
							team_liste+=[team]
							#print(date_str,team.liste_surnoms[0])
	except:
		print('echec recuperation')
		for team in Ligue1 :
			team_liste+=[team]
	return team_liste

#Classe pour gerer le tweet courant
liste_teams=liste_des_match()
class tweet :
	def __init__(self) :
		self.text=''
		self.liste_teams=liste_teams
	def next_tweet(self,text) :
		self.text=text
	#next_tweet(text)
	def check_teams(self) :
		print("Recherche attribution du tweet...")
		for team in self.liste_teams :
			if re.search(team.pattern,self.text) :
				print('Attribution du tweet a :  '+team.label)
				num_jour=time.localtime().tm_mday
				num_mois=time.localtime().tm_mon
				row=self.text+'~~'+str(time.time())
				print(row)
				team.add_tweet(row)
		return True


#Requete auto a twitter

def create_entity(liste_teams) :
	entity=["Ligue 1",'#Ligue1']
	for team in liste_teams :
		entity+=team.liste_surnoms
		print(team.liste_surnoms[0])
	#print(entity)
	return entity
	
	

#######Twitter

#Redressement des donnees
def pretrait(tweet):
	#Pour virer les liens
	tweet=re.sub(r'https?:[^\s]+','',tweet)
	#Pour remettre les accents
	tweet=re.sub(r'\\u00e8s?','e',tweet)
	tweet=re.sub(r'\\u00e0','a',tweet)
	tweet=re.sub(r'\\u00e7','c',tweet)
	tweet=re.sub(r'\\u00e9','e',tweet)
	tweet=re.sub(r'\\u00ea','e',tweet)
	tweet=re.sub(r'\\u00ee','i',tweet)
	tweet=re.sub(r'\\u00ef','i',tweet)
	tweet=re.sub(r'\\u00f4','o',tweet)
	tweet=re.sub(r'\\u00f9','u',tweet)
	tweet=re.sub(r'\\u00fb','u',tweet)
	tweet=re.sub(r'\n',' ',tweet)
	tweet=re.sub(r'\\u(0027|2019|00ab|00bb)',"'",tweet)
	tweet= unicodedata.normalize('NFKC', tweet)
	return tweet


#Sauver les tweets

#Outil de streaming
class Listener(StreamListener):
	def on_data(self, data):
		try:
			#print(data)
			raw=data.split(',"text":"')[1]
			raw = raw.split('","source')[0]
			tw=tweet()
			tw.text=pretrait(raw)
			#print(tw.text)
			tw.check_teams()
			print('fin trait tweet')
			save_tweets = tw.text
			save_tweets_file=open('out.csv','a+')
			save_tweets_file.write(tw.text)
			save_tweets_file.write('\n')
			save_tweets_file.close()
			return True
		except (BaseException, e):
			print("failed stream (rate limited?),", str(e))
			time.sleep(30)

	def on_error(self, status_code):
		if status_code == 420:
		#returning False in on_data disconnects the stream
			return False


def Record_Teams(liste_teams=liste_des_match()) :
	print("creation liste pour twitter.....\n")
	entity=create_entity(liste_teams)
	print("liste pour twitter ready\n")
	print('ouverture des fichiers tests.....')
	print("fichiers ouverts \n authentification....")
	ckey='Zs2DIvrMxTo2FiXYuMdxZSk4B'
	csecret='spf4uJJ7rHCWugi2TteegoTW1rr8HSr0oNAktMGaxObVr7zkGG'
	atoken='3065751124-Ge8ys1AxPZHsLWD1jKIXbB4gs1kDH8jkj30Ji24'
	asecret='SsMRdriSVb14ZQXi70BZYqhVXseHA4yOSUXuj3svJ2ts1'
	auth = tweepy.OAuthHandler(ckey,csecret)
	auth.set_access_token(atoken,asecret)
	api = tweepy.API(auth)
	public_tweets = api.home_timeline()
	print("launch stream....")
	twit_stream = Stream(auth, Listener())
	print("auth ok")
	twit_stream.filter(track=entity,async=True)
	print("Starting streaming !")



#Nettoyage
#~ for team in Ligue1:
	#~ f = open(team.tweet_ref('test'), "w+")
	#~ print('ok')
	#~ f.close()
