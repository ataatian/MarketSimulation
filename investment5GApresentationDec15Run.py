import numpy as np  #numerical and Matrix implementation
import pandas as pd #small database implementation
from pylab import *

nS=500 # total number of Runs of simulations 
nR=1000		#total number of Rounds for each Run 
I= 32.5
nInv=2
SecurityTypeN= 6
IntrValue= 37.5
OneSecTpye= 2
convRatio= 1.56
LpoolF= 80
LpoolI= 80

class InvsBank: 
	def __init__(self):
		self.N=LpoolF
		self.x=0 
		self.initialize()
		
	def initialize(self): 
	        self.InvsBankSecurityPool=np.floor(np.random.random(self.N)*SecurityTypeN) #builds the InvsBank Pool of securities
		self.currentType=-1 
		self.winnerID=-1 
		self.winnerPrice=-1
		self.bidders={}
		self.bids={}
		self.sx=-1
		self.Nproject= np.zeros(SecurityTypeN)
		
#some arrays to save data of each Round
		self.InvsBankProfit=-1*np.ones(nR)
		self.xArray=-1*np.ones(nR)
		self.sxArray=-1*np.ones(nR)
		self.winpriceArray=-1*np.ones(nR)
		self.winnerProfit=-1*np.ones(nR)
		self.securityType=-1*np.ones(nR)         #array: keeps the issued security type of each Rouns
		self.winnerIDArray=-1*np.ones(nR)
		
#some arrays to save data of each Run
		self.MemSecBestProf= -1*np.ones(SecurityTypeN) 
		self.MemSecLastBid= -1*np.ones(SecurityTypeN)
		self.MemSecSXmean= -1*np.ones(SecurityTypeN)

	def issue(self): 
		self.bids={}
		self.bidders={}
		#i=np.floor(self.N*np.random.random()) 
		#self.currentType=self.InvsBankSecurityPool[i]
		self.currentType= OneSecTpye     #just one type of security: equity!
                #####################################################################################
	def bid(self,ID, price):       #this function is called from outside
		i=len(self.bidders)
		self.bidders[i]=ID
		self.bids[i]=price 

	def findWinner(self):
	       self.winnerID= -1
	       self.winnerPrice= -1
	       self.MaxID=self.bidders[max(self.bids, key=self.bids.get)]
	       self.MaxPrice=max(self.bids.values())
	       if self.MaxPrice>=I:
		    self.winnerID= self.MaxID
                    self.winnerPrice=self.MaxPrice 



	def payReturn(self): 

		self.x=x=np.random.normal(50,2) #x is calculated  
		#self.x=x=np.random.uniform(0,100) #x is calculated  
		#self.x=x=50
		####################################################################################
		types={0:0, 1: min(x,50), 2:0.75*x, 3:x if x<86.6 else 0, 4:min(x,30)+0.96*max(x-50,0),5:min(max(x-10,0),60)+0.75*max(x-80,0)}
		self.sx=types[self.currentType]
		investors[self.bidders[self.winnerID]].RecieveInvReturn(self.sx)
		for i in range(len(investors)):
		    hh= -1*np.ones(nInv)
		    for j in range(nInv):
		        hh[j]= self.bids[j]
		    hh[i]= -1
		    MaxOfOthers=max(hh)
		    investors[i].invPoolsUpdate(self.sx,self.winnerPrice,self.bids[i],MaxOfOthers)  #here we call for all investors's learning
		self.currentInvsBankProfit= x+self.winnerPrice-(self.sx+I)
		
		#some arrays to save data of each Round
		self.InvsBankProfit[R]=self.currentInvsBankProfit
		self.xArray[R]=x
		self.sxArray[R]=self.sx
		self.winpriceArray[R]=self.winnerPrice
		self.winnerProfit[R]=self.sx-self.winnerPrice
		self.winnerIDArray[R]=self.bidders[self.winnerID]
		self.securityType[R]=self.currentType
		
		#some arrays to save data of each Run
		self.MemSecLastType= self.currentType
		self.MemSecLastBid[self.currentType]= self.winnerPrice
		self.Nproject[self.currentType]= self.Nproject[self.currentType]+1
		#self.MemSecLastSX[self.currentType]= self.sx
		
		self.MemSecSXmean[self.currentType]= (self.MemSecSXmean[self.currentType]*(self.Nproject[self.currentType]-1)+self.sx)/self.Nproject[self.currentType]

		#self.InvsBankPoolUpdate()   #here we call for InvsBank's learning

        def InvsBankPoolUpdate(self):
                #we apply learning by selection and mutation
                #Selection
                if self.MemSecBestProf[self.currentType]<self.currentInvsBankProfit:
                        self.MemSecBestProf[self.currentType]=self.currentInvsBankProfit
                MaxSec=max(enumerate(self.MemSecBestProf), key=(lambda x: x[1]))[0]
                MinSec=min(enumerate(self.MemSecBestProf), key=(lambda x: x[1]))[0]
                for i in range(self.N):
                    if self.InvsBankSecurityPool[i]== MinSec:
                        self.InvsBankSecurityPool[i]= MaxSec
                #Mutation
                for i in range(self.N):
                    if np.floor(np.random.random()*100)<=1: # 1 percent probability of mutation of a code
                        self.InvsBankSecurityPool[i]= np.floor(np.random.random()*SecurityTypeN)
                
	def getType(self):                        #this function is called from outside
		return self.currentType           #this function returns the security type choosed by the InvsBank

	def getProfit(self):                      #this function is called from outside
		return self.currentInvsBankProfit


class Investor: 
	def __init__(self):
		self.ID=len(investors)
		self.nP=LpoolI
		self.initialize()

	def initialize(self):
	        self.motherArray=np.floor(64*np.random.random((SecurityTypeN,self.nP)))
	        #self.motherArray= 63*np.ones((SecurityTypeN,self.nP))
	        ###################################################################################### initializtion of investors pricing strategies
		self.invStrategyPools={0:self.motherArray[0,:],1:self.motherArray[1,:],2:self.motherArray[2,:],3:self.motherArray[3,:],4:self.motherArray[4,:],5:self.motherArray[5,:]}
		self.bidPrice=-1
		self.BidSecType=-1
		
		#some arrays to save data of each Round
		self.invOwnProfit=-1*np.ones(nR)
		self.bidsArray=-1*np.ones(nR)
		self.sxArray=-1*np.ones(nR)
		self.StrgSumArray=-1*np.ones(nR)
			
	def placeBid(self):                 #picks a price from the coresponding security pool and places his bid
		self.BidSecType=InvsBank.getType()
		rn=np.floor(self.nP*np.random.random()) 
		self.bidPrice=convRatio*self.invStrategyPools[self.BidSecType][rn]
		self.bidsArray[R]=self.bidPrice
		InvsBank.bid(self.ID,self.bidPrice)

		self.StrgSum= {}
		for key,lis in self.invStrategyPools.items():
		    self.StrgSum[key] = sum(lis)
                self.StrgSumArray[R]=self.StrgSum[2]  ###########???????????????????????????????


	def RecieveInvReturn(self,sx):               #this function is called from outside
		self.sxArray[R]=sx
		self.invOwnProfit[R]=sx-self.bidPrice
		   
        
        def invPoolsUpdate(self,sx,WPrice,myPrice,OthersMax):
                #we apply learning by Selection, Crossover, Mutation and Election

                NewPool= np.zeros(self.nP)
                AssessProfit=np.zeros(self.nP)
                for i in range(self.nP):
                    AssessProfit[i]= sx-convRatio*self.invStrategyPools[self.BidSecType][i]
                    if self.invStrategyPools[self.BidSecType][i]<(OthersMax/convRatio):
                        AssessProfit[i]=0
                L= np.argsort(AssessProfit)
                for i in range(10):
                    self.invStrategyPools[self.BidSecType][L[i]]= self.invStrategyPools[self.BidSecType][L[self.nP-i-1]]
                #End of Selection

                
                for j in range(self.nP/2):
                    i1= np.floor(self.nP*np.random.random())
                    while True:
                        i2= np.floor(self.nP*np.random.random())
                        if i2==i1:
                            break
                    NewStrategy1=self.invStrategyPools[self.BidSecType][i1]
                    NewStrategy2=self.invStrategyPools[self.BidSecType][i2]
                    orgStrategy1=self.invStrategyPools[self.BidSecType][i1]
                    orgStrategy2=self.invStrategyPools[self.BidSecType][i2]
                    
                    #Crossover                
                    if np.floor(np.random.random()*100)<=60: # 60 percent probability of crossover of a code
                        strategy1= '{0:06b}'.format(int(orgStrategy1))
                        strategy2= '{0:06b}'.format(int(orgStrategy2))
                        CutPoint= int(np.floor(5*np.random.random()))+1  #somewhere between 1 to 5
                        NewStrategy1= int(strategy1[0:CutPoint]+strategy2[CutPoint:6],2)
                        NewStrategy2= int(strategy2[0:CutPoint]+strategy1[CutPoint:6],2)
                    
                    #Mutation
                    if np.floor(np.random.random()*100)<=.3: # 0.3 percent probability of mutation of a code                        
                        NewStrategy1= np.floor(np.random.random()*64)
                
                    if np.floor(np.random.random()*100)<=.3: # 0.3 percent probability of mutation of a code                        
                        NewStrategy2= np.floor(np.random.random()*64)
                    
                    #Election
                    LL= [NewStrategy1,NewStrategy2,orgStrategy1,orgStrategy2]
                    W=np.zeros(4)
                    for t in range(3):
                        W[t]= sx-convRatio*LL[t]
                        if LL[t]<(OthersMax/convRatio):
                            W[t]=0
                    K= np.argsort(W)
                    NewPool[2*j]= LL[K[3]]
                    NewPool[2*j+1]= LL[K[2]]
                self.invStrategyPools[self.BidSecType]= NewPool
	
	def getProfit(self):                     #this function is called from outside
		return self.invOwnProfit


#MAIN
close('all')
InvsBank=InvsBank()
investors={}
investorProfit={}
#building Investors 
for id in range(nInv):
	investors[id]=Investor() 
	investorProfit[id]=-1*np.ones(nR)


#these variables are for plotting of each Run
RunsLastSecType=-1*np.ones(nS)
RunsLastPool_2_PricesM=-1*np.ones(nS)
inv0=-1*np.ones(nS)
inv1=-1*np.ones(nS)
RunsLastSecPrices=-1*np.ones((SecurityTypeN,nS))
RunsSecSXmean=-1*np.ones((SecurityTypeN,nS))

#creating Rounds in each Run:
for s in range(nS):         #each Run starts
	InvsBank.initialize()	
	for ID in investors:
			investors[ID].initialize()
	for R in range(nR): #each Round starts
	        #print 'Round#: ', R
		InvsBank.issue()                         #InvsBank decides to raise fund for a project
		for ID in investors:                #investores decide to participate in the auction
			investors[ID].placeBid()
		InvsBank.findWinner()                    #InvsBank selects the winner and starts the project
		if InvsBank.winnerID<>-1:
		    InvsBank.payReturn()                    #InvsBank finishes the projects and returns the pay off to outside investors

	
	for id in range(len(investors)):
		investorProfit[id]=np.copy(investors[id].getProfit())
        
        #print 'ave sx', InvsBank.MemSecSXmean[2]
        RunsLastSecPrices[:,s]=InvsBank.MemSecLastBid    #the array of last winner prices for each security type in eash Run
        RunsSecSXmean[:,s]=InvsBank.MemSecSXmean    #the array of average payoff for each security type in eash Run
        RunsLastSecType[s]= InvsBank.MemSecLastType  #the last security type of each Run
        RunsLastPool_2_PricesM[s]=(investors[0].StrgSum[2]+investors[1].StrgSum[2])/(2*LpoolI)*convRatio
        
        inv0[s]=(investors[0].StrgSum[2])/(LpoolI)*convRatio
        inv1[s]=(investors[1].StrgSum[2])/(LpoolI)*convRatio
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #jj=0
        #Psx=-1*np.ones(nR)
        #Pwinprice=-1*np.ones(nR)
        #Pstrg0=-1*np.ones(nR)
        #Pstrg1=-1*np.ones(nR)
        #Pstrg=-1*np.ones(nR)
        #for i in range(nR):
        #        if InvsBank.winnerIDArray[i]==-1:
        #            continue
        #        Psx[jj]= InvsBank.sxArray[i]
        #        Pwinprice[jj]= InvsBank.winpriceArray[i]
        #        Pstrg0[jj]= investors[0].StrgSumArray[i]/LpoolI*convRatio
        #        Pstrg1[jj]= investors[1].StrgSumArray[i]/LpoolI*convRatio
        #        Pstrg[jj]= (Pstrg0[jj]+Pstrg1[jj])/2
        #        jj= jj+1
        #        
        #figure(1)
        #plot(range(jj),Psx[range(jj)])                     #payoffs of each Round
        #plot(range(jj),RunsSecSXmean[2,s]*np.ones(jj)) 
        #plot(range(jj),Pwinprice[range(jj)])               #winner price in each Round
        ##plot(range(jj),Pstrg0[range(jj)])                  #Ave of price strategies for inv0
        ##plot(range(jj),Pstrg1[range(jj)])                  #Ave of price strategies for inv1
        #plot(range(jj),Pstrg[range(jj)])                   #Ave of price strategies for inv0,1
        #legend(['Payoff (sx)','mean of sx','winner price','all investors Ave price strg'],fontsize=20)
        #ylim([0,100])
        #xlim([0, jj])
        #suptitle(['Round# %d ' %(nR),'Deal# %d ' %(jj)],fontsize=20)  
        #print 'Results for a single Run'
        #print 'Winner Prices mean: ',mean(Pwinprice)
        #print 'Security Intrinsic value (mean of S(x)): ',RunsSecSXmean[2,s]
        #print 'All Strg Mean: ',mean(Pstrg)      
        #
        #figure(2)
        #bar(range(nR),sign(InvsBank.winnerIDArray+1))
        #suptitle(['Round# %d ' %(nR),'Trade# %d ' %(jj)])  
        #ylim([0,5])
        #########################################################33
        ###########################################################

SecuritiesMean= mean(RunsLastSecPrices, axis=1)
SXMean= mean(RunsSecSXmean, axis=1)
Pool_2_M=mean(RunsLastPool_2_PricesM)

inv0Mean= mean(inv0)
inv1Mean= mean(inv1)



#plotting the ultimate prices for each security in each Run
j= OneSecTpye
figure(j+4)
plot(range(nS),SXMean[j]*np.ones(nS))
plot(range(nS),SecuritiesMean[j]*np.ones(nS))
plot(range(nS),Pool_2_M*np.ones(nS))
plot(range(nS),RunsLastSecPrices[j])
ylim([0,100])
legend(['Security Intrinsic value (mean of S(x))','Winner Prices mean','All Strg Mean','Security %d winner Prices' %(j)],fontsize=20)
suptitle(['Run# %d ' %(nS),'Round# %d ' %(nR), '%d investor(s)' %(nInv)],fontsize=20)

figure(j+5)

plot(range(nS),inv0Mean*np.ones(nS))
plot(range(nS),inv1Mean*np.ones(nS))
plot(range(nS),Pool_2_M*np.ones(nS))
ylim([0,100])
legend(['mean of Inv0 Price strg','mean of Inv1 Price strg','mean of all Price strg'],fontsize=20)
suptitle('Price Strategy Pools of Investors',fontsize=20)
#text(20,90,'HI')
#annotate(['local max'], xy=(10, 90))
show()

print 'Results for multiple simulations'
print 'Last Winner Prices mean: ',SecuritiesMean[j]
print 'Security Intrinsic value (mean of S(x)): ',SXMean[j]
print 'All last Strg Mean: ',Pool_2_M
print 'Winner Underpricing (%)',((SXMean[j]-SecuritiesMean[j])/SXMean[j])*100
print 'Price Strategies Underpricing (%)',((SXMean[j]-Pool_2_M)/SXMean[j])*100