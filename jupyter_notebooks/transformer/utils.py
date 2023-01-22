import pandas as pd
import tensorflow as tf

def add_spaces(x):
    return " ".join(x)

# We load the list, add a space between each letter and add an EOP (End of Passwort) Symbol pp. Since this is the only 2 letter "word" the EOP is unique.
def transform_password(df_in: pd.DataFrame) -> pd.DataFrame:
    return df_in[0].dropna().apply(lambda x: add_spaces(x) + ' eof' )

def pad_and_tokenize(sequences, tokenizer, max_length):
    return tf.keras.preprocessing.sequence.pad_sequences( tokenizer.texts_to_sequences(sequences) , maxlen = max_length, padding='pre')
