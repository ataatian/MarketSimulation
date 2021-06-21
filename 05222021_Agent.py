#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 20:46:30 2021

@author: Ali Taatian
"""
#### In this code I have implemented the market setup proposed by:   
##    Noe, Thomas H., Michael J. Rebello, and Jun Wang. "Corporate financing: An artificial agent‐based analysis." The Journal of Finance 58.3 (2003): 943-973.

########## House cleaning
import os
os.system('clear')

from IPython import get_ipython
get_ipython().magic('reset -sf')
#############

import numpy as np  #numerical and Matrix implementation
#import pandas as pd #small database implementation
#from pylab import *
import pylab

nS=3	        # total number of Runs of simulations 
nR=100		#total number of Rounds for each Run 
I= 32.5
nInv=2
SecurityTypeN= 6
IntrValue= 37.5
#R             #simulation Round number ( between 0 and nR for every simulaiton period)

class Firm: 
	def __init__(self):
		self.N=80
		self.x=0 
		self.initialize()

	def initialize(self):  
		self.firmSecurityPool= np.floor(np.random.random(self.N)*SecurityTypeN) 
		self.currentType=0 
		self.investorID=0 
		self.investorPrice=0
		self.bidders={}
		self.bids={}
		self.sx=0
		self.firmProfit=np.zeros(nR)
		self.xArray=np.zeros(nR)
		self.priceArray=np.zeros(nR)
		self.investorProfit=np.zeros(nR)
		self.securityType=np.zeros(nR)
		self.investorArray=-1*np.ones(nR)
		self.MemSecBestProf= -1*np.ones(SecurityTypeN) 
		self.MemSecLastBid= -1*np.ones(SecurityTypeN)

	def issue(self): 
		self.bids={}
		self.bidders={}
		i=np.floor(self.N*np.random.random()) 
		self.currentType=self.firmSecurityPool[int(i)]

	def bid(self,ID, price):       #this function is called from outside
		i=len(self.bidders)
		self.bidders[i]=ID
		self.bids[i]=price 

	def findWinner(self): 
		self.investorID=self.bidders[max(self.bids, key=self.bids.get)]
		self.investorPrice=max(self.bids.values())

	def payReturn(self): 
		if self.investorPrice<I:
			return 

		self.x=x=100.*np.random.random() #x is for simplicity  
		types={0:0, 1: min(x,50), 2:0.75*x, 3:x if x<86.6 else 0, 4:min(x,30)+0.96*max(x-50,0),5:min(max(x-10,0),60)+0.75*max(x-80,0)}
		self.sx=types[self.currentType]
		investors[self.bidders[self.investorID]].RecieveInvReturn(self.sx)
		for i in range(len(investors)):
		    if i!= self.bidders[self.investorID]:
		        investors[i].invPoolsUpdate(self.sx,self.investorPrice)  #here we call for other investors's learning
		
		self.currentFirmProfit= x-self.sx+self.investorPrice
		self.firmProfit[R]=x-self.sx+self.investorPrice
		self.xArray[R]=x
		self.priceArray[R]=self.investorPrice
		self.investorProfit[R]=self.sx-self.investorPrice
		self.investorArray[R]=self.bidders[self.investorID]
		self.securityType[R]=self.currentType
		self.MemSecLastBid[int(self.currentType)]= self.investorPrice
		self.firmPoolUpdate()   #here we call for firm's learning

	def firmPoolUpdate(self):
            #we apply learning by selection and mutation
            #Selection
            if self.MemSecBestProf[int(self.currentType)]<self.currentFirmProfit:
                    self.MemSecBestProf[int(self.currentType)]=self.currentFirmProfit
            MaxSec=max(enumerate(self.MemSecBestProf), key=(lambda x: x[1]))[0]
            MinSec=min(enumerate(self.MemSecBestProf), key=(lambda x: x[1]))[0]
            for i in range(self.N):
                if self.firmSecurityPool[i]== MinSec:
                    self.firmSecurityPool[i]= MaxSec
            #Mutation
            for i in range(self.N):
                if np.floor(np.random.random()*100)<=1: # 1 percent probability of mutation of a code
                    self.firmSecurityPool[i]= np.floor(np.random.random()*SecurityTypeN)
                
	def getType(self):                        #this function is called from outside
		return self.currentType           #this function returns the security type chosed by the firm

	def getProfit(self):                      #this function is called from outside
		return self.firmProfit


class Investor: 
	def __init__(self):
		self.ID=len(investors)
		self.nP=80
		self.initialize()

	def initialize(self):
		self.motherArray=np.floor(64*np.random.random((SecurityTypeN,self.nP)))
		self.invStrategyPools={0:self.motherArray[0,:],1:self.motherArray[1,:],2:self.motherArray[2,:],3:self.motherArray[3,:],4:self.motherArray[4,:],5:self.motherArray[5,:]}
		self.bidPrice=0
		self.BidSecType=0
		
		self.invOwnProfit=np.zeros(nR)
		self.bidsArray=np.zeros(nR)
		self.sxArray=np.zeros(nR)
			
	def placeBid(self):                 #picks a price from the coresponding security pool and places his bid
		self.BidSecType=firm.getType()
		rn=np.floor(self.nP*np.random.random()) 
		self.bidPrice=100/63*self.invStrategyPools[int(self.BidSecType)][int(rn)]
		self.bidsArray[R]=self.bidPrice
		firm.bid(self.ID,self.bidPrice)

	def RecieveInvReturn(self,sx):               #this function is called from outside
		self.sxArray[R]=sx
		self.invOwnProfit[R]=sx-self.bidsArray[R]
		self.invPoolsUpdate(sx,self.bidsArray[R])   #here we call for winner's learning     
        
	def invPoolsUpdate(self,sx,WPrice):
            #we apply learning by Selection, Crossover, Mutation and Election
            NewPool= np.zeros(self.nP)
            
            #Selection
            AssessProfit=np.zeros(self.nP)
            for i in range(self.nP):
                AssessProfit[i]= sx-self.invStrategyPools[self.BidSecType][i]
                if self.invStrategyPools[self.BidSecType][i]<=WPrice:
                    AssessProfit[i]=0
            L= np.argsort(AssessProfit)
            for i in range(10):
                self.invStrategyPools[self.BidSecType][L[i]]= self.invStrategyPools[self.BidSecType][L[self.nP-i-1]]

            for j in range(int(self.nP/2)):
                i1= np.floor(self.nP*np.random.random())
                while True:
                    i2= np.floor(self.nP*np.random.random())
                    if i2==i1:
                        break
                NewStrategy1=self.invStrategyPools[self.BidSecType][int(i1)]
                NewStrategy2=self.invStrategyPools[self.BidSecType][int(i2)]
                orgStrategy1=NewStrategy1
                orgStrategy2=NewStrategy2
                
                #Crossover                
                if np.floor(np.random.random()*100)<=60: # 60 percent probability of crossover of a code
                    strategy1= '{0:06b}'.format(int(NewStrategy1))
                    strategy2= '{0:06b}'.format(int(NewStrategy2))
                    CutPoint= int(np.floor(5*np.random.random()))+1  #somewhere between 1 to 5
                    NewStrategy1= int(strategy1[0:CutPoint]+strategy2[CutPoint:6],2)
                    NewStrategy2= int(strategy2[0:CutPoint]+strategy1[CutPoint:6],2)
                
                #Mutation
                if np.floor(np.random.random()*1000)<=3: # 0.3 percent probability of mutation of a code                        
                    NewStrategy1= np.floor(np.random.random()*64)
            
                if np.floor(np.random.random()*1000)<=3: # 0.3 percent probability of mutation of a code                        
                    NewStrategy2= np.floor(np.random.random()*64)
                
                #Election
                LL= [NewStrategy1,NewStrategy2,orgStrategy1,orgStrategy2]
                W=np.zeros(4)
                for t in range(3):
                    W[t]= sx-LL[t]
                    if LL[t]<=WPrice:
                        W[t]=0
                K= np.argsort(W)
                NewPool[2*j]= LL[K[3]]
                NewPool[2*j+1]= LL[K[2]]
            self.invStrategyPools[self.BidSecType]= NewPool
	
	def getProfit(self):                     #this function is called from outside
		return self.invOwnProfit


#MAIN
firm=Firm()
investors={}
investorProfit={}
#building Investors 
for id in range(nInv):
	investors[id]=Investor() 
	investorProfit[id]=np.zeros(nR)

GfirmProfit=np.zeros((nR,nS))
projectPayOff=np.zeros(nR)
BidPrice=np.zeros(nR)
InvWinnerProfit=np.zeros(nR)

RunsLastSecType=np.zeros(nS)
RunsLastSecPrices=np.zeros((SecurityTypeN,nS))
#creating Rounds in each Run:
for s in range(nS):         #each Run starts
	firm.initialize()
	
	for ID in investors:
			investors[ID].initialize()

	for R in range(nR): #each Round starts
		firm.issue()                         #firm decides to raise fund for a project
		for ID in investors:                #investores decide to participate in the auction
			investors[ID].placeBid()
			
		firm.findWinner()                    #firm selects the winner and starts the project
		firm.payReturn()                     #firm finishes the projects and returns the pay off to outside investors

	GfirmProfit[:,s]=np.copy(firm.getProfit())
	BidPrice=np.copy(firm.priceArray)
	projectPayOff=np.copy(firm.xArray)
	InvWinnerProfit=np.copy(firm.investorProfit)
	
	for id in range(len(investors)):
		investorProfit[id]=np.copy(investors[id].getProfit())
        
		RunsLastSecPrices[:,s]=firm.MemSecLastBid    #the array of last prices for each security in eash Run
		RunsLastSecType[s]= firm.securityType[nR-1]  #the last security type of each Run
		print (firm.MemSecLastBid)                  
		print (firm.securityType[nR-1]) 

SeciritiesMean= pylab.mean(RunsLastSecPrices, axis=1)
#print 


Allsx= investors[0].sxArray+investors[1].sxArray



pylab.close('all')
pylab.figure(3)
pylab.hist(RunsLastSecType)

#plotting the ultimate prices for each security in each Run
for j in range(SecurityTypeN):
    pylab.figure(j+4)
    pylab.plot(range(nS),RunsLastSecPrices[j])
    pylab.plot(range(nS),SeciritiesMean[j]*np.ones(nS))
    pylab.plot(range(nS),IntrValue*np.ones(nS))
    pylab.legend(['Security %d Prices' %(j),"Prices mean","Security Intrinsic value"])



pylab.figure(1)
pylab.plot(range(nR),projectPayOff)
pylab.plot(range(nR),BidPrice) 
pylab.plot(range(nR),InvWinnerProfit)
pylab.plot(range(nR),GfirmProfit)
pylab.legend(["Project PayOff(X)", "Bid Price(P)", "Investor Profit(Pi)","Firm Profit(Pf)"], loc=2)

pylab.figure(2)
pylab.plot(range(nR), firm.securityType)
pylab.plot(range(nR), firm.investorArray) 
pylab.legend(["Security Type", "Investor ID"]) 



pylab.show()


