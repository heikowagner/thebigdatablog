import keras.utils as ku 

def construct_subsequences(df, limit=None):
    '''
    We generate all possible observed sequences, the last letter is the letter to be predicted.
    This approach may allow the model to use the context of each line to help the model in those cases where a simple one-word-in-and-out model creates ambiguity.
    '''
    if not limit:
        limit = df.shape[0]
    sequences = []
    for row in df[:limit]:
        i=-1
        row_sequences = []
        for letter in row.split():
            if i>=0:
                if i>0:
                    row_sequences.append(row_sequences_dummy + [letter] )
                row_sequences_dummy = row_sequences_dummy + [letter]
            else:
                row_sequences_dummy=[letter]
            i=i+1
        sequences.append(row_sequences)
    return [num for elem in sequences for num in elem]

def ff_labels(tok_sequence, vocab_size):
    return ku.to_categorical(tok_sequence[:,-2], num_classes=vocab_size) , ku.to_categorical(tok_sequence[:,-1], num_classes=vocab_size)

def rnn_labels(tok_sequence, vocab_size):
    return tok_sequence[:,:-1], ku.to_categorical(tok_sequence[:,-1], num_classes=vocab_size)