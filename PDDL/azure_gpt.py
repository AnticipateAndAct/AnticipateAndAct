import re
import numpy as np
import math
from scipy.stats import kendalltau
import openai
import random
import time
from tqdm import tqdm
import json
from keyconfig import gpt_3, gpt_4

openai.api_type = "azure"
openai.api_base = "https://task-anticipation-gpt3.openai.azure.com/"    # ahana gpt 3.5

openai.api_version = "2023-03-15-preview"
openai.api_key = gpt_4
engine_name = 'ahana_gpt'

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

def kendal_tau(llm_routine, gt):
    missing = 0
    tau_val = []
    op_seq = {i: [] for i in sequences}
    gt_seq = {i: [] for i in sequences}
    for task in llm_routine:
        for seq in sequences:
            if task in sequences[seq]:
                op_seq[seq].append(task)

    for task in gt:
        for seq in sequences:
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
    try:
        tau = sum(tau_val)/len(tau_val)
    except:
        print("*****************************************")
        return 1,missing
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

def gpt_call(messages):
    response = openai.ChatCompletion.create(
        engine=engine_name,
        messages = messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    return response

def main(context, use_json):
    final_tau = []
    final_missing = []
    ordered_count = 0
    unordered_count = 0
    hallucination_count = 0
    missing_count = 0
    spot_on = 0
    task_count = 0
    hallucinations = []
    count = 0

    for count in tqdm(range(500)):
        while True:
            num_seq = 3
            if num_seq > 3:
                ip_seq = random.sample(sequences.keys(), num_seq)
                op_seq = random.sample(sequences.keys(), num_seq)
            else:        
                ip_seq = random.sample(sequences.keys(), num_seq)
                op_seq = list(set(sequences.keys()) - set(ip_seq))
                op_seq = random.sample(op_seq, num_seq)
            
            routine_day_1 = sample_tasks(sequences, ip_seq, sequence_probabilities, num_samples=num_seq, min_length=1, max_length=100)
            routine_day_2 = sample_tasks(sequences, op_seq, sequence_probabilities, num_samples=num_seq, min_length=1, max_length=100)

            all_sequences = [sequence for sub_sequence in sequences.values() for sequence in sub_sequence]
            combined_lists_ip_1 = [sequences[i][:2] for i in ip_seq[:num_seq]]
            combined_lists_ip_1 = sum(combined_lists_ip_1, [])

            combined_lists_op_1 = [sequences[i][2:] for i in ip_seq[:num_seq]]
            combined_lists_op_1 = sum(combined_lists_op_1, [])

            combined_lists_ip_2 = [sequences[i][:2] for i in op_seq[:num_seq]]
            combined_lists_ip_2 = sum(combined_lists_ip_2, [])

            combined_lists_op_2 = [sequences[i][2:] for i in op_seq[:num_seq]]
            combined_lists_op_2 = sum(combined_lists_op_2, [])

            final_seq = random.sample(sequences.keys(), num_seq)

            final_combined_lists_ip = [sequences[i][:1] for i in final_seq[:num_seq]]
            final_combined_lists_ip = sum(final_combined_lists_ip, [])

            final_combined_lists_op = [sequences[i][1:] for i in final_seq[:num_seq]]
            final_combined_lists_op = sum(final_combined_lists_op, [])
            
            task_count += len(final_combined_lists_op) + len(final_combined_lists_ip)

            prompt = f'''
```
# List of tasks:
tasks_sample_space = {task_dict if use_json else all_sequences}

# Consider the following routines:
routine_1 = {routine_day_1}
routine_2 = {routine_day_2}
# Anticipate a possible routine for routine 3
```

# Example Input
Anticipate the future tasks for routine 3 based on the following initial tasks
routine_3_input = {combined_lists_ip_1}
# Reasoning: The routine contains tasks for the following goals: {ip_seq}
# Example Output
```
routine_3_output = {combined_lists_op_1}
```

# Example Input
Anticipate the future tasks for routine 3 based on the following initial tasks
routine_3_input = {combined_lists_ip_2}
# Reasoning: The routine contains tasks for the following goals: {op_seq}
# Example Output
```
routine_3_output = {combined_lists_op_2}
```

# Input
Anticipate the future tasks for routine 3 based on the following initial tasks
routine_3_input = {final_combined_lists_ip}
# Output: 
'''
            if context==1:
                prompt = f'''
    ```
    # List of tasks:
    tasks_sample_space = {task_dict if use_json else all_sequences}

    # Consider the following routines:
    routine_1 = {routine_day_1}
    routine_2 = {routine_day_2}
    # Anticipate a possible routine for routine 3
    ```

    # Input
    Anticipate the future tasks for routine 3 based on the following initial tasks
    routine_3_input = {final_combined_lists_ip}
    # Reasoning: 
    # Output: 
    '''
            if context==2:
                prompt = f'''
    ```
    # List of tasks:
    tasks_sample_space = {task_dict if use_json else all_sequences}

    # Anticipate a possible routine for a day
    ```

    # Input
    Anticipate the future tasks for routine 3 based on the following initial tasks
    routine_3_input = {final_combined_lists_ip}
    # Reasoning: 
    # Output: 
    '''
            if context==3:
                prompt = f'''
    ```
    # List of tasks:
    tasks_sample_space = {task_dict if use_json else all_sequences}

    # Anticipate a possible routine for a day
    ```

    # Example Input
    Anticipate the future tasks for routine 3 based on the following initial tasks
    routine_3_input = {combined_lists_ip_1}
    # Reasoning: The routine contains tasks for the following goals: {ip_seq}
    # Example Output
    ```
    routine_3_output = {combined_lists_op_1}
    ```

    # Example Input
    Anticipate the future tasks for routine 3 based on the following initial tasks
    routine_3_input = {combined_lists_ip_2}
    # Reasoning: The routine contains tasks for the following goals: {op_seq}
    # Example Output
    ```
    routine_3_output = {combined_lists_op_2}
    ```

    # Input
    Anticipate the future tasks for routine 3 based on the following initial tasks
    routine_3_input = {final_combined_lists_ip}
    # Reasoning: 
    # Output: 
    '''
            # print(prompt)
            # exit()
            messages = [
                {
                    "role":"system",
                    "content":"You are an intelligent agent common househelp agent that anticipates future tasks based on previous days' data"
                },
                {
                    "role":"user",
                    "content":"Without any explanation, complete the following python script by adding your reasoning and anticipation for routine_3_output as a list:\n\n" + prompt
                }
            ]
            temp = 0.1
            
            response = gpt_call(messages)
            str1 = response["choices"][0]["message"]["content"]
            pattern = r'routine_3_output = \[(.*?)\]'
            output_line = re.search(pattern, str1)
            # print("output_line: ", output_line)

            if output_line:
                try:
                    routine_3_output = eval(output_line.group(1))
                    break
                except:
                    print("Not working")
            else:
                print("Not working")

        tau, missing = kendal_tau(routine_3_output, final_combined_lists_op)
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
        
        # Added because of prompting limit on gpt API key
        time.sleep(3)
        
    count = count + 1
    print(f'Context = {context}, use_json = {use_json}')
    print(f'Ordered count = {ordered_count}')
    print(f'Hallucination count = {hallucination_count}')
    # print(f'Missing count = {missing_count}')
    print(f'Unordered count = {unordered_count}')
    # print(f'Spot on = {spot_on}')
    print(f"Hallucinations = {hallucinations}")
    print(f"Average tau per prompt = {np.mean(final_tau)}")
    print(f"Average missing per prompt = {np.mean(final_missing)}")
    print(f'Total missing = {np.sum(final_missing)}')
    # print(count)
    print(f"Task count = {task_count}")
    print(f"Average task count = {task_count / count}")
    print(f'Total missing per task = {np.sum(final_missing) / task_count}')
    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    # print("\nWith context, no json")
    # main(True, False)
    print("\nWithout routines and without context and with json")
    main(2, True)
    print("\nWithout routines and with context examples and with json")
    main(3, True)
    # print("\nWith context and json")
    # main(0, True)
    print("\nWith routines without context and with json")
    main(1, True)