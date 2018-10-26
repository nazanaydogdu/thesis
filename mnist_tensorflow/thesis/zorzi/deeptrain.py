from mnist_tensorflow.thesis.zorzi.load_data import load_data
from mnist_tensorflow.thesis.zorzi.rbm_par import rbm_par
from mpi4py import MPI
import numpy as np
import time as time

def deeptrain(maxepoch):
    ''' MPI Init functions '''
    #MPI.Init()
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    siz = comm.Get_size()

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
    if (rank == 0):
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
        Proj = np.array([([numdims, sizelayer], numlayer, np.zeros(shape=(maxepoch, numlayer), dtype=int), totnum, batchsize, numbatches, siz, maxepoch, time.time())],
                 dtype = [('Layers', type(list)), ('nLayers', 'i4'), ('Err', type(np.ndarray)), ('nPatterns', 'i4'), ('Batchsize', 'i4'), ('nBatches', 'i4'), ('nCPU', 'i4'), ('nEpoch', 'i4'), ('Time', type(time))])

    '''Pretrains a deep network.'''
    WeightsLayer = {}

    #WeightsLayer = np.array(np.zeros((1, numlayer)), dtype=dict)
    for layer in range(numlayer):
    # run new RBM
        numhid = sizelayer[layer]
        rbm_par()

        if (rank == 0):
            # save the RBM weights
            rbmWeights = np.array([(layer, vishid, hidbiases, visbiases)],
                 dtype = [('layer', 'i4'), ('weight', 'i4'), ('hidbiases', type(np.ndarray)), ('visbiases', type(np.ndarray))])

            WeightsLayer[0, layer] = rbmWeights

            # update input data and parameters   for next layer
            batchdata = batchposhidprobs
            A = np.shape(batchdata)
            totnum = A[0] * A[2]
            numbatches = totnum / batchsize

    ''' SAVE Proj and WeightsLayer'''
    if (rank == 0):
        Proj["Time"] = time.time() - t
        fname = ['DeepNet_WORDS_' + str(batchsize) + '.npy']
        np.save(fname, 'Proj', 'WeightsLayer')