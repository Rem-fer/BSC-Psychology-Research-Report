import pandas as pd
import os


def get_inhibition_score(file_path):
    df = pd.read_csv(file_path)
    starting_index = df.index[df["ready.started"].notna()].to_list()[0]
    df_relevant = df.iloc[starting_index:]
    participant_id = os.path.basename(file_path).split('_')[0]
    correct_responses = df_relevant[(df_relevant['letter'] == 'X') & (df_relevant['response.corr'] > 0)]
    score = len(correct_responses)
    return participant_id, score

def process_all_files(folder_path):
    results = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            filepath = os.path.join(folder_path, file)
            participant_id, score = get_inhibition_score(filepath)
            results.append({'participant_id': participant_id, 'inhibition_score': score})
    return pd.DataFrame(results)



folder_path = '/Users/remyfernando/Desktop/Noguchi Active/BSc Psychology/Year 3/Research Project/Project data/Psychopy raw CSVs/'
inhibition_scores_df = process_all_files(folder_path)

# with open('inhibition_scores.csv', 'w') as f:
#     inhibition_scores_df.to_csv(f, index=False)

output_path = "/Users/remyfernando/Desktop/Noguchi Active/BSc Psychology/Year 3/Research Project/Project data/inhibition_scores.csv"
inhibition_scores_df.to_csv(output_path, index=False)