from django.http import HttpResponse
from django.shortcuts import render
from .models import Team, Ligue1, Record_Teams
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect

from .forms import NameForm

#from .cf import Team, Ligue1

def index(request):
	t = loader.get_template('Ligue1/index.html')
	form = NameForm()
	c = RequestContext(request, {'form': form})
	return HttpResponse(t.render(c))


def match(request):
	if request.method=='POST' :
		form=NameForm(request.POST)
		if form.is_valid() :
			equipe1=form.cleaned_data["equipe1"]
			equipe2=form.cleaned_data["equipe2"]
			liste_teams=[]
			for team in Ligue1:
				if team.label==equipe1 :
					print(team.label)
					team1=team
					liste_teams+=[team]
				if team.label==equipe2 :
					print(team.label)
					team2=team
					liste_teams+=[team]
			#Record_Teams(liste_teams)
			print(equipe1, equipe2)
			team1.data_to_classif_Bayes()
			team2.data_to_classif_Bayes()
			cote1=1+(team1.defa+team2.vic)/(team1.vic+team2.defa)
			cote2=1+(team1.vic+team2.defa)/(team1.defa+team2.vic)
			t = loader.get_template('Ligue1/match.html')
			c = RequestContext(request, {'equipe1': equipe1, 'equipe2' : equipe2,
			'cote1' : cote1, 'cote2' : cote2})
			return HttpResponse(t.render(c))
		else :
			return HttpResponse('il manque au moins un nom')
	