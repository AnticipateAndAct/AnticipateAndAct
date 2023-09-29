import json
import numpy as np
import math
from scipy.stats import kendalltau
from keyconfig import palm_api
import pprint
import google.generativeai as palm
import random
palm.configure(api_key=palm_api)

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

import random

f = open('task.json', 'r')
task_dict = json.load(f)
f.close()
f = open('sequences.json', 'r')
sequences = json.load(f)
f.close()

agentless_tasks = [
    "Run the washing machine",
    "Dry the clean clothes",
    "Preheat the oven",
    "Bake in the oven",
    "Serve food",
    "Run the dishwasher",
    "Remove cake from the oven",
    "Vacuum the floors",
]

sequence_probabilities = {
    "Cooking": 0.8,
    "Washing clothes": 0.4,
    "Washing dishes": 0.7,
    "Cleaning the house": 0.5,
    "Gardening": 0.2,
    "Baking": 0.2
}

def kendal_tau(llm_routine, gt, local_seq):
    missing = 0
    tau_val = []
    op_seq = {i: [] for i in local_seq}
    gt_seq = {i: [] for i in local_seq}
    for task in llm_routine:
        for seq in local_seq:
            if task in sequences[seq]:
                op_seq[seq].append(task)

    for task in gt:
        for seq in local_seq:
            if task in sequences[seq]:
                gt_seq[seq].append(task)

    op_seq = {k: v for k, v in op_seq.items() if v}
    gt_seq = {k: v for k, v in gt_seq.items() if v}
    keys_not_in_op_seq = set(gt_seq) - set(op_seq)
    for key in keys_not_in_op_seq:
        missing += len(gt_seq[key])

    for key in op_seq.keys():
        str1 = op_seq[key]
        try:
            str2 = gt_seq[key]
        except:
            continue

        temp = [x for x in str2 if x not in set(str1)]
        if len(temp)>0:
            missing += len(temp)
            print("Missing\n", temp)

        # Taking intersections while retaining the ordering
        var1 = list(x for x in str1 if x in set(str2))
        var2 = list(x for x in str2 if x in set(str1))
        # Remove duplicates
        var1 = list(dict.fromkeys(var1))

        rank_mapping = {val: rank + 1 for rank, val in enumerate(sequences[key])}
        rank1 = [rank_mapping[val] for val in var1]
        rank2 = [rank_mapping[val] for val in var2]

        if len(var1) <= 1:
            tau = 1
        else:
            try:
                tau, p_value = kendalltau(rank1, rank2)
            except ValueError:
                import pdb; pdb.set_trace()

            if math.isnan(tau):
                print("**********************NAN**********************")
                import pdb; pdb.set_trace()

        tau_val.append(tau)

    # missing = missing/len(gt)
    tau = sum(tau_val)/len(tau_val)
    if math.isnan(tau):
        import pdb; pdb.set_trace()
    return tau, missing

def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True

def sanity_check(routine, sequences):
    op_seq = {i: [] for i in sequences}
    for task in routine:
        for seq in sequences:
            if task in sequences[seq]:
                op_seq[seq].append(task)
    
    ordered = []
    for seq in op_seq:
        if not op_seq[seq]:
            continue
        indices = []
        for task in op_seq[seq]:
            indices.append(sequences[seq].index(task))
        if not is_sorted(indices):
            print(f'{seq} is not sorted')
            print(op_seq[seq])
            return False
        else:
            ordered.append(True)

    return True

def sample_tasks(sequences, seq_names, sequence_probabilities, num_samples=3, min_length=15, max_length=20):
    
    # Sample sequences
    # selected_sequences = sample_sequences(sequences, sequence_probabilities, num_samples, min_length, max_length)
    selected_sequences = sorted(seq_names, key=lambda item: sequence_probabilities[item], reverse=True) # Sort based on their probabilities (meaning importance)
    local_seq = {
        selected_sequences[i]: sequences[selected_sequences[i]] for i in range(len(selected_sequences))
    }

    hold_seq = {
        selected_sequences[i]: [False, 0] for i in range(len(selected_sequences))
    }

    # Total number of tasks in the selected sequences
    num_tasks = sum(len(tasks) for tasks in local_seq.values())

    # Initialize the number of tasks sampled from each sequence
    tasks_sampled = {selected_sequences[i]: 0 for i in range(len(selected_sequences))}

    count = 0
    routine = []
    while count<num_tasks:
        if all(value[0] for value in hold_seq.values()):
            # All sequences are on hold
            random_key = random.choice(list(hold_seq.keys()))
            hold_seq[random_key][0] = False
            # Randomly put one sequence off hold

        # Select a sequence that is not on hold
        seq = next((element for element in selected_sequences if not hold_seq[element][0]), None)
        
        try:
            assert seq is not None
        except AssertionError:
            import pdb; pdb.set_trace()

        # Get the id of the task to be sampled from the current sequence
        task_id = tasks_sampled[seq]
        try:
            task = local_seq[seq][task_id]
            routine.append(task)
        except IndexError:
            # Completed all tasks in the current sequence
            selected_sequences.remove(seq)
            del hold_seq[seq]
            continue

        tasks_sampled[seq] += 1 
        count += 1

        if task in agentless_tasks:
            hold_seq[seq] = [True, 0]

        for seq in hold_seq:
            if hold_seq[seq][0] == True:
                if hold_seq[seq][1] < 2:
                    hold_seq[seq][1] += 1
                else:
                    hold_seq[seq][0] = False

    return routine


def main():
    results = {}
    temperatures = [0.1, 0.01, 0.5, 0.9]
    for palm_temp in temperatures:
        final_tau = []
        final_missing = []
        unordered_count = 0
        hallucination_count = 0
        missing_count = 0
        spot_on = 0
        task_count = 0
        ordered_count = 0
        hallucinations = []
        count = 0

        while count<500:
            while True:
                num_seq = 4
                if num_seq > 3:
                    ip_seq = random.sample(sequences.keys(), num_seq)
                    op_seq = random.sample(sequences.keys(), num_seq)
                else:        
                    ip_seq = random.sample(sequences.keys(), num_seq)
                    op_seq = list(set(sequences.keys()) - set(ip_seq))
                    op_seq = random.sample(op_seq, num_seq)
                
                routine_day_1 = sample_tasks(sequences, ip_seq, sequence_probabilities, num_samples=num_seq, min_length=15, max_length=20)
                routine_day_2 = sample_tasks(sequences, op_seq, sequence_probabilities, num_samples=num_seq, min_length=15, max_length=20)

                all_sequences = [sequence for sub_sequence in sequences.values() for sequence in sub_sequence]
                random.shuffle(all_sequences)
                combined_lists_ip_1 = [sequences[i][:2] for i in ip_seq[:num_seq]]
                combined_lists_ip_1 = sum(combined_lists_ip_1, [])

                combined_lists_op_1 = [sequences[i][2:] for i in ip_seq[:num_seq]]
                combined_lists_op_1 = sum(combined_lists_op_1, [])

                combined_lists_ip_2 = [sequences[i][:2] for i in op_seq[:num_seq]]
                combined_lists_ip_2 = sum(combined_lists_ip_2, [])

                combined_lists_op_2 = [sequences[i][2:] for i in op_seq[:num_seq]]
                combined_lists_op_2 = sum(combined_lists_op_2, [])

                final_seq = random.sample(sequences.keys(), num_seq)

                final_combined_lists_ip = [sequences[i][:2] for i in final_seq[:num_seq]]
                final_combined_lists_ip = sum(final_combined_lists_ip, [])

                final_combined_lists_op = [sequences[i][2:] for i in final_seq[:num_seq]]
                final_combined_lists_op = sum(final_combined_lists_op, [])

                prompt = f'''
# List of tasks:
tasks_sample_space = {task_dict}

# Example Input
routine_3_input = {combined_lists_ip_1}
# Reasoning: The routine contains tasks for the following goals: {ip_seq}
# Example Output
routine_3_output = {combined_lists_op_1}

# Example Output
routine_3_input = {combined_lists_ip_2}
# Reasoning: The routine contains tasks for the following goals: {op_seq}
# Example Output
routine_3_output = {combined_lists_op_2}

# Input
routine_3_input = {final_combined_lists_ip}
# Reasoning: 
# Output:
'''
                completion = palm.generate_text(
                    model=model,
                    prompt=prompt,
                    temperature=palm_temp,
                    # The maximum length of the response
                    max_output_tokens=1000,
                    # candidate_count = 8
                )

                if completion.result:
                    print("Working temp = ", palm_temp)
                    break
                else:
                    # PaLM does not return an output some times for some identified reason. Prompting again with the same parameters seems to work though.
                    print("Not working temp = ", palm_temp)
            for candidate in completion.candidates[:1]:
                task_count += len(final_combined_lists_op) + len(final_combined_lists_ip)
                code_to_execute = candidate['output'].strip()  # Removing triple quotes

                env = {}
                try:
                    exec(code_to_execute, env)
                except Exception as e:
                    print(e)
                    continue
                
                try:
                    routine_3_output = env['routine_3_output']
                except:
                    print('Error in execution?')
                    try:
                        routine_3_output = eval(code_to_execute)
                    except:
                        print('Error in execution.')
                        import pdb; pdb.set_trace()
                        continue
                tau, missing = kendal_tau(routine_3_output, final_combined_lists_op, final_seq)
                final_tau.append(tau)
                final_missing.append(missing)
                all_sequences = [sequence for sub_sequence in sequences.values() for sequence in sub_sequence]

                temp = [x for x in routine_3_output if x not in set(all_sequences)]

                if len(temp) > 0:
                    hallucination_count += 1
                    hallucinations.extend(temp)

                sanity = sanity_check(routine_3_output, sequences)
                if sanity:
                    ordered_count += 1
                else:
                    unordered_count += 1

                count += 1

                print(count)

            
        results[palm_temp] = {  
            'Average Ordered count': ordered_count / count,
            'Average Hallucination count': hallucination_count / count,  
            'Average Missing count': missing_count / count,  
            'Average Unordered count': unordered_count / count,  
            'Average Hallucinations': len(hallucinations) / count,  
            'Average tau per prompt': np.mean(final_tau),  
            'Average missing per prompt': np.mean(final_missing),  
            'Total missing': np.sum(final_missing),  
            'Average task count': task_count / count  
        }

    for temp, result in results.items():  
        print(f'Temperature: {temp}')  
        for key, value in result.items():  
            print(f'{key}: {value}')  
        print('\n')  

if __name__ == '__main__':
    main()