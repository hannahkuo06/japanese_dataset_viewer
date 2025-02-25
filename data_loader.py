import pandas as pd
import streamlit as st
from datasets import load_dataset
from huggingface_hub import login

dataset_name = "ServiceNow-AI/japanese_data"

def load_data(token):
    login(token=token)
    # If successful, update session state to reflect that the user is authenticated
    st.session_state.authenticated = True
    st.write("You are logged in!")
    dataset = load_dataset(dataset_name, "japanese_general_inst_following", split="train", batch_size=1000)
    return st.session_state.authenticated, dataset

def get_data_generator(dataset, batch_size=100):
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