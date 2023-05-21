import os
import numpy as np
import pandas as pd
from time import time
from Bio import SeqIO
import pickle
import shogun as sg


# Best sample length found in experiments
downstream_size = 240
upstream_size = 36

script_dir = os.path.dirname(os.path.abspath(__file__))
model_file = os.path.join(script_dir,'circTIS_model_v1.pkl')


# Extract a subsequence around a TIS from circRNA, according length windows. 
# If necessary, loops through the circRNA to complete total sample length.
def extract_circrna_subseq_around_position(circrna_seq, length_window_left, length_window_right, TIS_start_position_zi):

    up_subseq = circrna_seq[:TIS_start_position_zi]
    down_subseq = circrna_seq[TIS_start_position_zi:]

    window_left = up_subseq
    while len(window_left) < length_window_left:
        window_left = circrna_seq + window_left
    window_left = window_left[-length_window_left:]

    window_right = down_subseq
    while len(window_right) < length_window_right:
        window_right = window_right + circrna_seq
    window_right = window_right[:length_window_right]

    full_window = window_left + window_right

    return full_window


def extract_samples(fasta_file_path, tis_types):

    df_samples = pd.DataFrame(columns=['circRNA_id', 'TIS_type', 'position'])
    samples = []
    n_seqs = 0

    with open(fasta_file_path) as handle:

        for record in SeqIO.parse(handle, "fasta"):

            n_seqs += 1

            circrna_id = record.id
            circrna_seq = str(record.seq)
            circrna_length = len(circrna_seq)

            for position_zi in range(circrna_length-3):  # position_zi = position zero indexed
                
                test_codon = circrna_seq[position_zi:position_zi+3]

                if test_codon in tis_types:

                    df_samples.loc[df_samples.shape[0]] = [circrna_id, test_codon, position_zi+1]  # index correction
                    sample = extract_circrna_subseq_around_position(circrna_seq, upstream_size, downstream_size, position_zi)
                    samples.append(sample)

    return df_samples, samples, n_seqs


def svm_predict(X):

    start_time = time()

    with open(model_file, "rb") as f:
        svm = pickle.load(f)

    # Creating Shogun features objects
    X_sg = sg.StringCharFeatures(sg.DNA)
    X_sg.set_features(X)
    
    # Predicting
    prediction = svm.apply(X_sg)
    y_pred_labels = prediction.get_labels()
    y_pred_scores = prediction.get_values()
    
    # Converting scores to probabilities using the sigmoid function
    y_pred_probs = 1 / (1 + np.exp(-y_pred_scores))

    end_time = time()
    pred_time = end_time - start_time

    return y_pred_labels, y_pred_scores, y_pred_probs, pred_time
