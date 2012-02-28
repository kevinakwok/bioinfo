import sys


f = open ("Sequences.txt","r")
output = open('Output.txt', 'w')
seqB = f.readline()
seqA = f.readline()

seqB = seqB[:-1]

seqA = "-"+seqA
seqB = "-"+seqB

#Sets the values for match, mismatch, and gap.
match = 1
mismatch = 0
gap = -1

row = len(seqA)
col = len(seqB)

#Function to print out matrix. Used for testing.
def print_matrix():
    for i in range(row):
        print("{}".format(A[i]))

#Creates blank matrix
def create_matrix(row,col):
    A = [0] * row
    for i in range(row):
        A[i] = [0] * col
    return A

def isMatch(i,j):
    if seqA[i] == seqB[j]:
        matchVal = match
    else:
        matchVal = mismatch
    return matchVal

#Returns the new value if diagonal is used
def diag(i,j):
    return A[i-1][j-1] + isMatch(i,j)

#Returns the new value if up is used
def up(i,j):
    return A[i-1][j] + isMatch(i,j) + gap

#Returns the new value if left is used
def left(i,j):
    return A[i][j-1] + isMatch(i,j) + gap

#Fills matrix with correct scores.
def complete_matrix(row,col):
    for i in range(1,row):
        for j in range(1,col):
            A[i][j] = max(0,diag(i,j),up(i,j),left(i,j))
    return A

#FInd the highest scoring cell.
def get_max(A):
    local_max = [[0,0]]
    for i in range(row):
        for j in range(col):
            if A[i][j] == A[local_max[0][0]][local_max[0][1]]:
                local_max.append([i,j])
            elif A[i][j] > A[local_max[0][0]][local_max[0][1]]:
                local_max = [[i,j]]
    return local_max

#Gives you the next location.
def get_next(A,location):
    i = location[0]
    j = location[1]
    maxVal = max(A[i-1][j-1],A[i-1][j]+gap,A[i][j-1]+gap)
    if A[i-1][j-1] == maxVal:
        return [i-1,j-1]
    #Is this the right ordering of the three?
    elif A[i][j-1]+gap == maxVal:
        return [i,j-1]
    else:
        return [i-1,j]

#Traces the path back given starting location
def trace_back(A,tracer):
    if A[tracer[len(tracer)-1][0]][tracer[len(tracer)-1][1]] == 0:
        return tracer
    next_cell = get_next(A,tracer[len(tracer)-1])
    #tracer.insert(0,next_cell)
    tracer.append(next_cell)
    return trace_back(A,tracer)

#Uses tracer to return final sequence
def get_seq(A,tracer,k,seq):
    if k == 0:
        original_sequence = seqA
    else:
        original_sequence = seqB
    N = len(tracer)
    for i in range(0,N-1):
        if tracer[i][k] == tracer[i+1][k]+1:
            seq = seq + original_sequence[tracer[i][k]]
        elif tracer[i][k] == tracer[i+1][k]:
            seq = seq + "-"
    return seq

#Shows the relevant lines for matching pairs
def get_middle(finalA,finalB):
    middle = ""
    for k in range(len(finalA)):
        mid = " "
        if finalA[k] == finalB[k]:
            mid = "|"
        middle = middle + mid
    return middle

A = create_matrix(row,col)

A = complete_matrix(row,col)

num_answers = len(get_max(A))

for i in range(num_answers):
    tracer = trace_back(A,[get_max(A)[i]])
    #print A[get_max(A)[i][0]][get_max(A)[i][1]]
    finalA = get_seq(A,tracer,0,"")
    finalB = get_seq(A,tracer,1,"")
    finalA = finalA[::-1]
    finalB = finalB[::-1]
    middle = get_middle(finalA,finalB)
    #print tracer
    #print("{}\n{}\n{}\n".format(finalA,middle,finalB))
    output.write("{}\n{}\n{}\n\n".format(finalA,middle,finalB))

print "Algorithm run successfully"
#print_matrix()