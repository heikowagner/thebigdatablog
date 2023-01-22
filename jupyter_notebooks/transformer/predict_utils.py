from keras import Sequential
from keras.preprocessing.text import Tokenizer
import matplotlib.pyplot as plt
from data_preparation import add_spaces, pad_and_tokenize
import numpy as np

def plt_props(vals, preds):
    f = plt.figure()
    f.set_figwidth(20)
    plt.bar(vals, preds, width=0.9)
    plt.show()

def predict_letter(vocabular:list, propabilities:list, plot:bool=False)->dict:
    """Performs a random choice out of the vocabular based on the passed propabilities."""
    if plot:
        plt_props(vocabular, propabilities[0])
    return np.random.choice( vocabular , 1, p=propabilities[0])[0]

def predict_next_letter(previous_letters: str, model: Sequential, tokenizer: Tokenizer, plot:bool=False ) -> str:
    max_length = model.get_config()["layers"][0]["config"]["batch_input_shape"][1]
    previous_letters = list(map(add_spaces, [previous_letters]))
    tok_prev = pad_and_tokenize(previous_letters, tokenizer, max_length)
    propabilities = model.predict(tok_prev)
    predicted_letter = predict_letter(['eof'] + list(tokenizer.index_word.values()) , list(propabilities), plot)
    return predicted_letter


def predict_password(previous_letters: str, model: Sequential, tokenizer: Tokenizer) -> str:
    password = previous_letters
    new_letter=""
    while True:
        new_letter = predict_next_letter(password, model, tokenizer)
        if new_letter == "eof":
            break
        password = password + new_letter
    return password