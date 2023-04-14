#!/usr/bin/env python3

# circTIS predicts TIS in circRNA sequences
# Author: Denilson Fagundes Barbosa (denilsonfbar@gmail.com)

import os
import datetime as dt
from optparse import OptionParser
import libcirctis as lct


def __main__():

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", 
                      help=
                      '''mandatory - input circRNAs file (FASTA format). Ex: 
                      example/circRNA_seqs.fa''', 
                      metavar="file", default=None)
    parser.add_option("-t", "--tis", dest="tis", 
                      help=
                      '''optional - TIS types for search. Options:
                      ATG                                                    
                      NC1 [ATG, CTG, GTG, TTG]                               
                      NC2 [ATG, CTG, GTG, TTG, AAG, ACG, AGG, ATA, ATC, ATT]
                      [default = NC1]''',
                      metavar="string", default="NC1")
    parser.add_option("-o", "--output", dest="output_folder", 
                      help=
                      '''optional - path to output folder. Ex:
                      path/to/output_folder                                             
                      if not declared, it will be created at the circRNAs 
                      input folder                                       
                      [default = "circTIS_output"]''', 
                      metavar="folder", default=None)
    (options, args) = parser.parse_args()
    
    if options.file == None:
        print("""
circTIS v1.0

Use -h for help. 
Basic example to find TIS in circRNA sequences:

python3 circtis.py -f example/circRNA_seqs.fa

        """)
        quit()

    if options.file != None and os.path.isfile(options.file) == False:
        print("The circRNAs file indicated is not a valid file.")
        print('Please, indicate a valid FASTA file to the \"-f\" option.')
        quit()

    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" -> started circTIS v1.0")
    
    if options.tis == 'ATG':
        tis_types = ['ATG']
    elif options.tis == 'NC1':
        tis_types = ['ATG', 'CTG', 'GTG', 'TTG']
    elif options.tis == 'NC2':
        tis_types = ['ATG', 'CTG', 'GTG', 'TTG', 'AAG', 'ACG', 'AGG', 'ATA', 'ATC', 'ATT']

    if options.output_folder == None:
        options.output_folder = ""
        folder_l = options.file.split("/")
        for i in range(0, len(folder_l)-1):
            options.output_folder += str(folder_l[i])+"/"
        options.output_folder += "circTIS_output/"
    elif options.output_folder.endswith("/") == False:
        options.output_folder += "/"
    if os.path.isdir(options.output_folder) == False:
        os.mkdir(options.output_folder)
    
    # Samples extraction
    df_samples, samples, n_seqs = lct.extract_samples(options.file, tis_types)

    # Prediciton
    y_pred_labels, y_pred_scores, y_pred_probs, pred_time = lct.svm_predict(samples)
    print(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" -> prediction finished")

    # Saving results
    df_samples['svm_score'] = y_pred_scores
    df_samples['probability'] = y_pred_probs
    df_samples.to_csv(options.output_folder+'all_possible_TIS.tsv', sep='\t', index=False)
    
    df_samples_pos = df_samples[df_samples['probability'] > 0.5]
    df_samples_pos.to_csv(options.output_folder+'predicted_TIS.tsv', sep='\t', index=False)

    print("Number of input sequences -> " + str(n_seqs))
    print("Number of predicted TIS   -> " + str(len(df_samples_pos)))
    print("All possible TIS file     -> " + options.output_folder + "all_possible_TIS.tsv")
    print("Predicted TIS file        -> " + options.output_folder + "predicted_TIS.tsv")


__main__()
