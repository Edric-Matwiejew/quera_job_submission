import json
import matplotlib.pyplot as plt
from collections import Counter

results_path="#############"

with open(results_path, 'r') as json_file:
    results = json.load(json_file)

# Filter 'post_sequence' based on 'pre_sequence' and 'shot_status'
post_selected_results = [
    shot['post_sequence'] 
    for shot in results['shot_outputs'] 
    if shot['pre_sequence'] == [1, 1] and shot['shot_status'] == 'Completed'
]

print(f'{len(post_selected_results)} of {len(results["shot_outputs"])} shots post-selected.')

post_sequence_tally = Counter(tuple(seq) for seq in post_selected_results)

labels, counts = zip(*post_sequence_tally.items())
labels = [''.join(map(str, label)) for label in labels]

plt.bar(labels, counts)
plt.xlabel('State')
plt.ylabel('Shots')
plt.show()
