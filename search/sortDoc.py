import cmath
def getScoreDocList(index,fileNum, words,docList):
    scoreDocList = []
    for doc in docList:
        score = get_wfidf_Score(index,fileNum,doc,words)
        #scoreDocList 是score和doc的list
        scoreDocList.append([score,doc])
    #print(scoreDocList)
    return scoreDocList

#从大到小得到sortedDocList
def sortScoreDocList(index,fileNum,words,docList):
    scoreDocList = getScoreDocList(index,fileNum,words,docList)
    return sorted(scoreDocList,reverse = True)

#堆排序实现的top K查询
def TopKScore(K,index,fileNum,words,docList):
    scoreDocList = getScoreDocList(index, fileNum, words, docList)
    N = len(scoreDocList)
    if N is 0:
        return []
    scoreDocList = heapsort(scoreDocList,N,K)
    L = K
    if N < K: L = N
    return [scoreDocList[N - x - 1] for x in range(0,L)]


def leftChild(i):
    return 2 * i + 1

def percDown(A,i,N):
    tmp = A[i]
    while leftChild(i) < N:
        child = leftChild(i)
        if child != N - 1 and A[child+1][0] > A[child][0]:
            child += 1
        if tmp[0] < A[child][0]:
            A[i] = A[child]
        else:
            break
        i = child
    A[i] = tmp
    return A

def heapsort(A,N,K):
    i = int(N / 2)
    while i >= 0:
        A = percDown(A,i,N)
        i -= 1
    i = N - 1
    end = 0
    if N - 1 > K:
        end = N - 1 - K
    while i > end:
       tem = A[0]
       A[0] = A[i]
       A[i] = tem
       percDown(A,0,i)
       i -= 1
    return A


def get_tfidf(index, fileNum , docID, word) :
    docID = str(docID)
    if docID not in index[word]:
        return "0"
    tf = len(index[word][docID])
    df = len(index[word])
    idf = cmath.log10(fileNum / df).real
    return tf * idf

def get_wfidf(index, fileNum, docID, word):
    docID = str(docID)
    if docID not in index[word]:
        return "0"
    tf = len(index[word][docID])
    df = len(index[word])
    wf = 1 + cmath.log10(tf).real
    idf = cmath.log10(fileNum / df).real
    return wf * idf

def get_wfidf_Score(index,fileNum,docID,wordList):
    score = 0
    docID = str(docID)
    for word in wordList:
        if word not in index or docID not in index[word]:
            continue
        tf = len(index[word][docID])
        df = len(index[word])
        wf = 1 + cmath.log10(tf).real
        idf = cmath.log10(fileNum / df).real
        temp=wf * idf
        # temp=adjust(word,temp,docID)
        score += temp
    return score

def get_tfidf_Score(index,fileNum,docID,wordList):
    score = 0
    docID = str(docID)

    for word in wordList:

        if word not in index or docID not in index[word]:
            continue
        tf = len(index[word][docID])
        df = len(index[word])
        idf = cmath.log10(fileNum / df).real
        # print("filenum / df",fileNum / df, "df: ",df, " idf: ", idf )
        score += tf * idf
    return score
