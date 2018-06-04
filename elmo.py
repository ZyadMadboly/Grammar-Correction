# Need allennlp with torch==0.3.1 && GPU

from allennlp.modules.elmo import Elmo, batch_to_ids
from helper import *
import pickle

options_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_options.json" 
weight_file = "https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

elmo = Elmo(options_file, weight_file, 2, dropout=0)

def loadConll(path='CoNLL_data/train.txt'):
    # Read the file and split into lines
    path='CoNLL_data/train.txt'
    lines = open(path, encoding='utf-8').read().strip().split('\n')

    # Split every line into pairs and normalize and then split to words
    pairs = [[[e for e in normalizeString(s).split(' ')] for s in l.split('\t')] for l in lines]
    return pairs

def elmoFromPair(pair):
    # choose layer 2 representations
    layer = 1
    character_ids = batch_to_ids(pair)
    input_tensor, output_tensor = elmo(character_ids)['elmo_representations'][layer].data
    return (input_tensor, output_tensor)

# input_lang, output_lang, pairs = prepareData('eng', 'fra', True)
if __name__ == '__main__':
    emb_path = 'CoNLL_data/train.elmo'

    # subset
    pairs = loadConll()[:10]
    # pairs = [[['First', 'sentence', '.'], ['Another', '.']]]

    embeddings = [elmoFromPair(pair) for pair in pairs]
    with open(emb_path, 'wb') as file:
        pickle.dump(embeddings, file)
