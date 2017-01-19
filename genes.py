import sys
import operator
from collections import defaultdict
from math import log, exp
from random import randint
import copy
from copy import deepcopy

genomelength = 264
firstmovestart = 8
generationsize = 20
fitness_scaling= 2

class player:
	def __init__(self):
		self.genome = makegenome()
		self.lastmove = self.genome[-firstmovestart:]
		self.score = 0
		self.tourneyscore = 0
		self.fitness = 0
		self.isnice = isitnice(self)
		self.numrep = 0

class T4Tplayer:
	def __init__(self):
		self.genome = makeTFTgenome()
		self.lastmove = self.genome[-firstmovestart:]
		self.score = 0
		self.tourneyscore = 0
		self.fitness = 0
		self.isnice = isitnice(self)
		self.numrep = 0

def isitnice(self):
	if self.genome[ geneindex(self.lastmove) ] == 'C':
		return True
	else:
		return False
#makes a player corresponding to the TIT FOR TAT strategy
def makeTFTgenome():
	s=""
	i=0
	while (i<genomelength):
		if i%2 == 0:
			s = s + 'D'
		else:
			s = s + 'C'
		i+=1
	return s
#generates a random strategy genome ie, string of Cs and Ds
def makegenome():
	player = ""
	for i in range(genomelength):
		x = randint(0,1)
		if x == 1:
			player = player + 'C'
		else:
			player = player + 'D'

	return player
#returns the index within the genome of the strategy to play
def geneindex(totranslate):
	binarystring = ""
	for i in range(len(totranslate)):
		if totranslate[i] == 'C':
			binarystring = binarystring + '1'
		elif totranslate[i] == 'D':
			binarystring = binarystring + '0'

	index = int(binarystring, 2)
	#print index
	return index

#updates the last move a player has made
def updatelastmove(player, playermove, coplayermove):
	player.lastmove = player.lastmove[2:] + playermove + coplayermove
#simulates a game of the iterated Prisonner's Dilemma 
def PDgame(player1, player2):
	#clear their scores
	player1.score = 0
	player2.score = 0
	#players load their first move from the end of the genome
	player1.lastmove = player1.genome[-firstmovestart:]
	player2.lastmove = player2.genome[-firstmovestart:]
	#get its correspond strategy out of their genome
	p1M = player1.genome[ int ( geneindex(player1.lastmove) )]
	p2M = player2.genome[ int ( geneindex(player2.lastmove) )]

	#print player1.score, player2.score, p1M, p2M
	gameover = False
	roundsplayed = 0

	while ( gameover == False ):
		#score players for their moves
		if (p1M == 'C') and (p2M == 'C'):
			player1.score = player1.score + 3
			player2.score = player2.score + 3
		if (p1M == 'C') and (p2M == 'D'):
			player1.score = player1.score + 0
			player2.score = player2.score + 5
		if (p1M == 'D') and (p2M == 'C'):
			player1.score = player1.score + 5
			player2.score = player2.score + 0
		if (p1M == 'D') and (p2M == 'D'):
			player1.score = player1.score + 1
			player2.score = player2.score + 1

		updatelastmove(player1, p1M, p2M)
		updatelastmove(player2, p2M, p1M)

		#print player1.score, player2.score, p1M, p2M
		p1M = player1.genome[ geneindex(player1.lastmove) ]
		p2M = player2.genome[ geneindex(player2.lastmove) ]
		roundsplayed+=1
		if roundsplayed == 200:
			gameover = True

def makegeneration( numplayers):
	generation = []
	for i in range(numplayers):
		generation.append( player() )
	return generation

def tourneysort(player):
	return player.tourneyscore

def printgen(gen):
	for i in range( len(gen) ):
		print gen[i].genome

def generationtourney( generation ):

	for i in range( len(generation) ):
		iscore = 0
		for j in range( len(generation) ):
			if i != j:
				PDgame(generation[i], generation[j] )
				iscore = iscore + generation[i].score
		generation[i].tourneyscore = iscore

	generation = sorted( generation, key=tourneysort)
	maxscore = max(player.tourneyscore for player in generation)
	minscore = min(player.tourneyscore for player in generation)
	sumscore = sum(player.tourneyscore for player in generation)
	avscore = sumscore/ len(generation)

	computefitness(generation, minscore, maxscore, avscore)


	return generation

def computefitness(generation, mini, maxi, avrg):

	if (mini == maxi) and (avrg == maxi):
		for i in range( len(generation) ):
			generation[i].fitness = -56
		return
	minfit = -1
	if minfit < 0 :
		#print "rescale"
		a = float(avrg) / float(avrg - mini)
		b = float( -1 * mini) * float(avrg) / float(avrg-mini)
		##print a, b
		for i in range( len(generation) ):
			generation[i].fitness = a * generation[i].tourneyscore + b

	return
#select parents for spawning
def selectparents(generation):
	totalfitness = 0
	for i in range( len(generation) ):
		totalfitness = totalfitness + generation[i].fitness
	#print "totalfitness", totalfitness

	p1 = randint(0, int(totalfitness) )
	p2 = randint(0, int(totalfitness) )
	p1 = p1 -1
	p2 = p2 -1
	ind1 = 0
	ind2 = 0
	x = -1
	y = -1
	while ind1 <= p1:
		x+=1
		ind1 += generation[x].fitness
	while ind2 <= p2:
		y+=1
		ind2 += generation[y].fitness

	return(generation[x], generation[y], x, y)
#produces two children from two parents
def spawn( mates ):
	# we're using crossover at a random index in the genome
	split = 1 
	while(split%2 != 0):
		split = randint(0, genomelength ) 

	chile1 = player()
	chile2 = player()

	chile1.genome = mates[0].genome[:split] + mates[1].genome[split:]
	chile1.lastmove = chile1.genome[-firstmovestart:]
	chile1.isnice = isitnice(chile1)

	chile2.genome = mates[1].genome[:split] + mates[0].genome[split:]
	chile2.lastmove = chile2.genome[-firstmovestart:]
	chile1.isnice = isitnice(chile2)

	return(chile1, chile2)
#makes next generation
def breednextgen(generation):

	nextgen = []
	while (len(nextgen) ) < (len (generation) ):
		pair = selectparents(generation)
		attempts = 0
		while(pair[0].numrep >=2 or pair[1].numrep >=2) and (attempts <= 0 ):
			attempts +=1
			pair = selectparents(generation)
		children = spawn( pair )
		nextgen.append( children[0] )
		nextgen.append( children[1] )
		generation[ pair[2] ].numrep+=1
		generation[ pair[3] ].numrep+=1

	return nextgen

def avgscore(gen):
	sumscore = sum(player.tourneyscore for player in gen)
	avscore = sumscore/ len(gen)
	return avscore
#evolution simulation where environment is the evolving generation
def evolutionsimulation_self():

	primus = makegeneration(20)
	print "Beginning simulation"
	i = False
	gen1 = primus
	c = 0
	while(i ==False):
		c+=1
		#print i
		gen1 = generationtourney(gen1)
		#print avgscore(gen1)
		if gen1[0].fitness==-56:
			i = True
		if (i == False):
			gen2 = breednextgen(gen1)
			gen1 = gen2

	printstablegame(gen1, c)
	stabilitytest(gen1[0], c)
	return gen1[0]
	
#tests the stability of a population
def stabilitytest(goon, c):
	PDgame(goon, goon)
	goonscore = goon.score
	challengerscore = 0
	t= 0
	while(challengerscore < goonscore) and (c < 5000):
		c+=1
		t+=1
		challenger = player()
		PDgame(goon, challenger)
		challengerscore = challenger.score

	if (t < generationsize):
		print "population is not particularly robust having been invaded by the ",t,"th random challenger"

	if (c == 5000):
		print "population is stable!! (most likely)"
		print "the first 5000 random opponents could not obtain better scores from interacting with population member than between pop members"
	elif (t > c):
		print "population is moderately robust, obtains better scores within itself than with first", t," random opponents"


#prints the game between two players from the converged population
def printstablegame(gen1, c):
	print "Algorithm converged after ",c," rounds"
	print"Below is an example of a typical game played between two players in our converge environment:"
	printPDgame( gen1[0],gen1[1] )
	PDgame(gen1[0], gen1[1] )
	print "Final scores of ", gen1[0].score, gen1[1].score 

def printPDgame(player1, player2):
	#clear their scores
	player1.score = 0
	player2.score = 0
	#players load their first move from the end of the genome
	player1.lastmove = player1.genome[-firstmovestart:]
	player2.lastmove = player2.genome[-firstmovestart:]
	#get its correspond strategy out of their genome
	p1M = player1.genome[ int ( geneindex(player1.lastmove) )]
	p2M = player2.genome[ int ( geneindex(player2.lastmove) )]

	#print player1.score, player2.score, p1M, p2M
	gameover = False
	roundsplayed = 0
	x=""
	y=""
	while ( gameover == False ):
		x = x+p1M
		y = y+p2M

		updatelastmove(player1, p1M, p2M)
		updatelastmove(player2, p2M, p1M)

		#print player1.score, player2.score, p1M, p2M
		p1M = player1.genome[ geneindex(player1.lastmove) ]
		p2M = player2.genome[ geneindex(player2.lastmove) ]
		roundsplayed+=1
		if roundsplayed == 200:
			gameover = True
	print "PLAYER1: ", x
	print "PLAYER2: ", y

	cooperations = 0
	defections = 0
	for character in x:
		if character == 'C':
			cooperations +=1
		if character == 'D':
			defections += 1
	coop_ratio = float(cooperations)/roundsplayed
	defect_ratio = float(defections)/roundsplayed

	print cooperations, defections, coop_ratio, defect_ratio, roundsplayed

	print "Ratio of cooperations:", coop_ratio
	print "Ratio of defections:", defect_ratio


def PDgameNOISE(player1, player2):

	#clear their scores
	player1.score = 0
	player2.score = 0
	#players load their first move from the end of the genome
	player1.lastmove = player1.genome[-firstmovestart:]
	player2.lastmove = player2.genome[-firstmovestart:]
	#get its correspond strategy out of their genome
	p1M = player1.genome[ int ( geneindex(player1.lastmove) )]
	p2M = player2.genome[ int ( geneindex(player2.lastmove) )]

	#print player1.score, player2.score, p1M, p2M
	gameover = False
	roundsplayed = 0

	while ( gameover == False ):
		r1 = randint(1, 6)
		r2 = randint(1, 6)

		if r1 == 6:
			if p1M == 'C':
				p1M = 'D'
			else:
				p1M = 'C'
		if r2 == 6:
			if p2M == 'C':
				p2M = 'D'
			else:
				p2M = 'C'

		#score players for their moves
		if (p1M == 'C') and (p2M == 'C'):
			player1.score = player1.score + 3
			player2.score = player2.score + 3
		if (p1M == 'C') and (p2M == 'D'):
			player1.score = player1.score + 0
			player2.score = player2.score + 5
		if (p1M == 'D') and (p2M == 'C'):
			player1.score = player1.score + 5
			player2.score = player2.score + 0
		if (p1M == 'D') and (p2M == 'D'):
			player1.score = player1.score + 1
			player2.score = player2.score + 1

		updatelastmove(player1, p1M, p2M)
		updatelastmove(player2, p2M, p1M)

		#print player1.score, player2.score, p1M, p2M
		p1M = player1.genome[ geneindex(player1.lastmove) ]
		p2M = player2.genome[ geneindex(player2.lastmove) ]
		roundsplayed+=1
		if roundsplayed == 200:
			gameover = True

def generationtourneyTFT( generation ):

	TFT = T4Tplayer()

	for i in range( len(generation) ):
		iscore = 0
		PDgameNOISE(generation[i], TFT )
		iscore = iscore + generation[i].score
	#		print "won", generation[i].score, iscore
	#	print "player", i, "has score", iscore
		generation[i].tourneyscore = iscore

	generation = sorted( generation, key=tourneysort)
	maxscore = max(player.tourneyscore for player in generation)
	minscore = min(player.tourneyscore for player in generation)
	sumscore = sum(player.tourneyscore for player in generation)
	avscore = sumscore/ len(generation)
	#print minscore, maxscore, avscore, "made it"

	if(minscore==maxscore):
		printgen(generation)

	computefitnessTFT(generation, minscore, maxscore, avscore)

	return generation

def evolutionsimulation_TFTN():

	primus = makegeneration(20)
	print "Beginning simulation"
	primal = copy.deepcopy(primus)
	gen1 = primus
	c = 0
	i = False
	avgs = []
	while(c < 1000):

		c+=1
		gen1 = generationtourneyTFT(gen1)
		avgs.append( avgscore(gen1) )
		#if ( c < 204 ):
		gen2 = breednextgenTFT(gen1)
		gen1 = gen2

	analyzeNOISE(primal, gen1)
	#return (gen1, avgs)

def analyzeNOISE(primus, finalgen):
	stratlength = genomelength - firstmovestart

	TFTC = stratlength/2
	TFTD = stratlength/2
	pC=0
	fgC=0
	pD=0
	fgD=0
	for p in range(len(primus)):
		for i in range(stratlength):
			if i%2 == 0:
				if primus[p].genome[i] == 'D':
					pD+=1
				if finalgen[p].genome[i] == 'D':
					fgD+=1
			else:
				if primus[p].genome[i] == 'C':
					pC+=1
				if finalgen[p].genome[i] == 'C':
					fgC+=1
	pC = pC/generationsize
	fgC = fgC/generationsize
	pD = pD/generationsize
	fgD = fgD/generationsize

	print "first generation shared ", float(pC)/float(TFTC) ,"percent Cooperations with TFT"	
	print "final generation shared ", float(fgC)/float(TFTC), "percent Cooperations with TFT"
	print "first generation shared ", float(pD)/float(TFTD), "percent Defections with TFT"	
	print "final generation shared ", float(fgD)/float(TFTD), "percent Defections with TFT"

def computefitnessTFT(generation, mini, maxi, avrg):
	for i in range( len(generation) ):
		generation[i].fitness = generation[i].score

def breednextgenTFT(generation):

	nextgen = []

	while (len(nextgen) ) < (len (generation) ):
		pair = selectparents(generation)
		children = spawn( pair )
		nextgen.append( children[0] )
		nextgen.append( children[1] )

	return nextgen
