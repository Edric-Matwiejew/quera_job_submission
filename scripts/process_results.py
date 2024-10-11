'''@brief  This script shows how you can process a json file produced by submitting to Aquila 
(or the bloqade backends).

* Note that we are NOT importing bloqade here but it could be useful in some circumstances. 
* Note that there is no API for directly pulling from the dashboard used by QuEra so you have 
to download the json results file somewhere before processing it. 
'''

import json
import matplotlib.pyplot as plt
from collections import Counter

# Filter 'post_sequence' based on 'pre_sequence' and 'shot_status'
def FilterPostSequence(results : dict, desired_pre_sequence : list):
    '''Filter the results dictionary so that it only contains the output of shots that were successfully completed
    and had the desired initial state
    '''
    post_selected_results = list()
    if results['task_status'] != 'Completed': 
        return post_selected_results
    
    post_selected_results = [
        shot['post_sequence'] 
        for shot in results['shot_outputs'] 
        if shot['pre_sequence'] == desired_pre_sequence and shot['shot_status'] == 'Completed'
    ]
    return post_selected_results


# load data and filter 
results_path="#############"
desired_pre_sequence = [1,1]
with open(results_path, 'r') as json_file:
    results = json.load(json_file)
    post_selected_results = FilterPostSequence(results, desired_pre_sequence])
    print(f'{len(post_selected_results)} of {len(results["shot_outputs"])} shots post-selected.')

# plot results 
post_sequence_tally = Counter(tuple(seq) for seq in post_selected_results)
labels, counts = zip(*post_sequence_tally.items())
labels = [''.join(map(str, label)) for label in labels]
plt.bar(labels, counts)
plt.xlabel('State')
plt.ylabel('Shots')
plt.show()
