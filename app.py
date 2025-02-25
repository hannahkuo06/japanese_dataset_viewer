import random

import streamlit as st

from data_loader import load_data


def display_conversation(selected_record):
    convo = selected_record.get("conversation")
    for turn in convo:
        if turn["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f"User: {turn['content']}")
        elif turn["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(f"Assistant: {turn['content']}")
        elif turn["role"] == "system":
            with st.chat_message("system"):
                st.markdown(f"System: {turn['content']}")


st.title("Japanese Dataset Viewer")

batch_generator = load_data()
batches = list(batch_generator)  # Collect all batches into a list (for pagination)
num_batches = len(batches)

# Ensure session state for batch_index and record_index
if "batch_index" not in st.session_state:
    st.session_state.batch_index = 0
if "current_record_index" not in st.session_state:
    print("true")
    st.session_state.current_record_index = 0


batch_options = [i for i in range(num_batches)]
selected_batch = st.selectbox("Select a batch to view", batch_options,
                              index=st.session_state.batch_index,)

st.session_state.batch_index = selected_batch  # Extract batch number from the string

batch = batches[st.session_state.batch_index]

record_options = [i for i in range(len(batch))]
selected_record_index = st.selectbox("Select a conversation to view", record_options,
                                     index=st.session_state.current_record_index,)
st.session_state.current_record_index = selected_record_index  # Extract record number from the string

# Streamlit App Layout
# Navigation buttons to move through the records
if st.button("Next"):
    # Increment the current_record_index and possibly batch_index
    print("current batch:", st.session_state.batch_index)
    print("current record:", st.session_state.current_record_index)
    if st.session_state.current_record_index < len(batch) - 1:
        st.session_state.current_record_index += 1
    else:
        # Move to next batch and reset record to 0
        st.session_state.current_record_index = 0
        if st.session_state.batch_index < num_batches - 1:
            st.session_state.batch_index += 1
        else:
            # Loop back to the first batch
            st.session_state.batch_index = 0

    # Update batch and record based on the session state
    batch = batches[st.session_state.batch_index]
    selected_record = batch.iloc[st.session_state.current_record_index]

    # Display the selected conversation
    st.write(f"Currently Viewing: Batch {st.session_state.batch_index}, Record {st.session_state.current_record_index}")

    st.subheader("Conversation:")
    display_conversation(selected_record)

if st.button("Random"):
    # Randomly select a batch and record within the valid range
    random_batch_index = random.randint(0, num_batches - 1)
    random_record_index = random.randint(0, len(batches[random_batch_index]) - 1)

    # Update the session state with the random values
    st.session_state.batch_index = random_batch_index
    st.session_state.current_record_index = random_record_index

    # Get the randomly selected batch and record
    batch = batches[st.session_state.batch_index]
    selected_record = batch.iloc[st.session_state.current_record_index]

    # Display the random conversation
    st.write(f"Currently Viewing [RANDOM]: Batch {st.session_state.batch_index}, Record {st.session_state.current_record_index}")
    st.subheader("Conversation:")
    display_conversation(selected_record)

else:
    # Get the selected batch and record for the normal view
    batch = batches[st.session_state.batch_index]
    selected_record = batch.iloc[st.session_state.current_record_index]

    # Display the selected conversation
    st.write(f"Currently Viewing: Batch {st.session_state.batch_index}, Record {st.session_state.current_record_index}")
    st.subheader("Conversation:")
    display_conversation(selected_record)
