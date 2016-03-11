from flask import render_template, request
from . import app, db, redis_db
import json
from tables import open_file
from sqlalchemy import text
import os
from numpy import argmax, zeros, log, exp, sum
from numpy.random import multinomial
from random import randint 
from keras.models import model_from_json

base_dir = os.path.dirname(__file__)
start_samples = open_file(base_dir + "/static/data/pres_start_samples.hdf", driver="H5FD_CORE").root.start_samples[:]
n_words = start_samples.shape[1]
with open(base_dir + '/static/data/indicies_to_char.json', 'r') as fp:
    indicies_to_char = json.load(fp)
with open(base_dir + '/static/data/char_to_indicies.json', 'r') as fp:
    char_to_indicies = json.load(fp)
model = model_from_json(open(base_dir + '/static/data/candidate_model_architecture.json').read())
model.load_weights(base_dir + '/static/data/candidate_lstm_weights.h5')


@app.route("/gen_seed_text/")
def gen_seed_text():
    index_val = randint(0, len(start_samples) - 1)
    selected_row = start_samples[index_val, :, :]
    text = []
    for w in range(n_words)[1:]:
        index_char = argmax(selected_row[w, :])
        text.append(indicies_to_char[str(index_char)])
    text_string = ' '.join(text)
    return json.dumps(text_string)


@app.route("/gen_cand_text/", methods=['POST'])
def gen_cand_text():
    seed_text = request.json['seed_text']
    seed_text = "<START> " + seed_text
    seed_text_list = seed_text.split(" ")
    gen_text = gen_sentence_from_seed(seed_text_list)
    gen_sentence = " ".join(gen_text)
    json_data = {'gen_text': gen_sentence}
    return json.dumps(json_data)


def sample(a, temperature=1.0):
    # helper function to sample an index from a probability array
    # take log of probabilities
    a = log(a) / temperature
    # convert back to probabilities
    a = exp(a) / sum(exp(a))
    # Sample one given the probabilities and get that index
    return argmax(multinomial(1, a, 1))


def gen_sentence_from_seed(seed_text):
    generated = []
    sentence = seed_text
    # don't show <start>
    generated.extend(sentence[1:])

    next_char = ""
    while next_char != "<END>":
        x = zeros((1, 5, len(char_to_indicies.keys())))
        for t, char in enumerate(sentence):
            x[0, t, char_to_indicies[char]] = 1.

        preds = model.predict(x, verbose=0)[0]
        next_index = sample(preds, 1.0)
        next_char = indicies_to_char[str(next_index)]

        # generated keeps track of text im generating
        generated.append(next_char)
        # sentence shifts down by 1 for next loop
        sentence = sentence[1:]
        sentence.append(next_char)
    return generated[:-1]


@app.route("/talk_like_pres_candidate/")
def talk_like_pres_candidate():
    sections = [
        {
            'href': '/',
            'name': 'Blog'
        },
        {
            'href': '/resources/',
            'name': 'Data Science Resources'
        },
        {
            'href': '/#about',
            'name': 'About/Contact'
        }
    ]
    return render_template("/talk_pres/talk_like_pres_cand.html", sections=sections)
