from mnist_tensorflow.thesis.zorzi.load_data import load_data
import numpy as np
import time as time

def deeptrain(maxepoch):
    '''deep network parameters'''
    sizelayer=[30, 60, 120] # a vector
    numlayer = len(sizelayer)
    batchsize = 10

    '''RBM parameters'''
    epsilonw = 0.1;   # Learning rate for weights
    epsilonvb = 0.1;   # Learning rate for biases of visible units
    epsilonhb = 0.1;   # Learning rate for biases of hidden units
    weightcost = 0.0002;
    initialmomentum = 0.5;
    finalmomentum = 0.9;

    '''load training data'''
    [inputdata, targets] = load_data() # Load datafiles and constructs a big input / output matrix
    numdims = len(inputdata[0]) # Input size : column number
    tardims = len(targets[0]) # Size of target encoding: column number
    totnum = len(inputdata) # totnum: total number of training patterns: row number
    # rand('state', 0);
    randomorder = np.random.permutation(range(totnum)) #
    numbatches = int(np.ceil(totnum / batchsize) )# Make batches of this size
    batchdata = np.zeros(shape=(batchsize, numdims, numbatches)) # Prepare matrixes with batches.All data will be here.
    batchtargets = np.zeros(shape=(batchsize, tardims, numbatches))
    A = [batchsize, numdims, numbatches]; # Batch - matrix.NUMBATCHES will be parceled into more processors

    '''Distribute data'''
    for b in range(numbatches): # Prepare input and output batch data
        batchdata[:,:, b] = inputdata[[randomorder[range(b * batchsize, (b + 1) * batchsize)]], :]
        batchtargets[:,:, b] = targets[[randomorder[range(b * batchsize, (b + 1) * batchsize)]], :]

    '''Clear original data'''
    del inputdata, targets

    t = time.time()
    # STORE PROJECT INFO
    Proj = {
    "Layers": [numdims, sizelayer],
    "nLayers": numlayer,
    "Err": np.zeros(shape=(maxepoch, numlayer)),
    "nPatterns": totnum,
    "Batchsize": batchsize,
    "nBatches": numbatches,
    "nEpoch": maxepoch
    }

deeptrain(10)