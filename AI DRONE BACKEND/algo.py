import itertools



def sub_lists(list1): 
    sublist = [[]] 
    for i in range(len(list1) + 1):  
        for j in range(i + 1, len(list1) + 1): 
            sub = list1[i:j] 
            sublist.append(sub)               
    return sublist 

def findsubsets(s, n): 
    return list(itertools.combinations(s, n))

def assignDrones(DroneSpace,itemspace):
    DroneSpace = DroneSpace
    itemspace = itemspace
    print("Drone Weights are : ",DroneSpace)
    print("Items to be Delivered are :",itemspace)
    itemsleft = itemspace.copy()
    visited=[]
    answer=[]
    for i in range(0,len(DroneSpace)):
        answer.append(0)
    alreadyadded=[]
    for i in range(0,len(DroneSpace)):
        alreadyadded.append(0)
    

    l1 = [1, 2, 3, 4] 
    for i in range(0,len(DroneSpace)):
        visited.append(0)
    itemspace = sorted(itemspace,reverse=True)
    sumDrone = sum(DroneSpace)
    sumItem = sum (itemspace)

    MasterItem = []
    for i in range (0,len(itemspace)+1):
        MasterItem = MasterItem + findsubsets(itemspace,i)
    totItem = len(MasterItem)
    totItemList = []
    templist = []
    for i in range(0,len(MasterItem)):
        MasterItem[i]=list(MasterItem[i])
    ItemsSubset=MasterItem.copy()
    for i in range(0,len(MasterItem)):
        MasterItem[i]=sum(MasterItem[i])
    for i in range(0,len(MasterItem)):
        if(MasterItem[i]>DroneSpace[0]):
            MasterItem[i]=0
            ItemsSubset[i]=0
    MasterItem=list(filter(lambda a: a != 0, MasterItem))
    ItemsSubset=list(filter(lambda a: a != 0, ItemsSubset))
    ItemsSubset=ItemsSubset[1:]

    def isEmpty():
        for i in range(0,len(MasterItem)):
            if(MasterItem[i]!=0):
                return False
        return True

    while(isEmpty()==False):
        for i in range(0,len(MasterItem)-1):
            for j in range(i+1,len(ItemsSubset)):
                if(MasterItem[i]<MasterItem[j]):
                    MasterItem[i],MasterItem[j]=MasterItem[j],MasterItem[i]
                    ItemsSubset[i],ItemsSubset[j]=ItemsSubset[j],ItemsSubset[i]
        i=0
        pos=-1
        weight=MasterItem[i]
        for j in range(0,len(DroneSpace)):
            if (weight<=DroneSpace[j] and visited[j]==0):
                pos=j
                if(alreadyadded[j]==1):
                    break
        if(pos==-1):
            break
        if(ItemsSubset[i]==0):
            continue
        answer[pos]=ItemsSubset[i]
        DroneSpace[pos]-=weight
        alreadyadded[pos]=1
        subsets=sub_lists(ItemsSubset[i])
        subsets.remove([])
        for v in range(0,len(ItemsSubset[i])):
            itemsleft.remove(ItemsSubset[i][v])
        ItemsSubset=[]
        for v in range (0,len(itemsleft)+1):
            ItemsSubset = ItemsSubset + findsubsets(itemsleft,v)
        for v in range(0,len(ItemsSubset)):
            ItemsSubset[v]=list(ItemsSubset[v])
        MasterItem=ItemsSubset.copy()
        for v in range(0,len(MasterItem)):
            MasterItem[v]=sum(MasterItem[v])
        max=0
        for v in range(0,len(DroneSpace)):
            if(max<DroneSpace[v]):
                max=DroneSpace[v]
        for v in range(0,len(MasterItem)):
            if(MasterItem[v]>max):
                MasterItem[v]=0
                ItemsSubset[v]=0
        MasterItem=list(filter(lambda a: a != 0, MasterItem))
        ItemsSubset=list(filter(lambda a: a != 0, ItemsSubset))
        ItemsSubset=ItemsSubset[1:]
    print("Final Answer is : ",answer)
    return answer