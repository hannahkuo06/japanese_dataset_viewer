import pandas as pd
from datasets import load_dataset

dataset_name = "ServiceNow-AI/japanese_data"
dataset = load_dataset(dataset_name, "japanese_general_inst_following", split="train", batch_size=1000)

def load_data(dataset, batch_size=100):
    total_rows = len(dataset)
    num_batches = total_rows // batch_size + (1 if total_rows % batch_size != 0 else 0)

    for i in range(num_batches):
        # Get a batch (slice the dataset)
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_rows)
        batch = dataset[start_idx:end_idx]

        # Convert to DataFrame
        df_batch = pd.DataFrame(batch)
        yield df_batch

def get_data():
    return dataset