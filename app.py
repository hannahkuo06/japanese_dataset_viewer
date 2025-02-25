import random

import streamlit as st

from data_loader import get_data_generator, load_data

# Initialize session state if it doesn't exist
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'dataset' not in st.session_state:
    st.session_state.dataset = None

# Allow users to input their Hugging Face token
huggingface_token = st.text_input("Enter your Hugging Face Token:")

# Check if token is provided and authenticate
if huggingface_token and not st.session_state.authenticated:
    try:
        st.session_state.authenticated, st.session_state.dataset = load_data(huggingface_token)

    except Exception as e:
        st.error(f"Authentication failed: {e}")

# If the user is authenticated, show some other content (e.g., model interaction)
if st.session_state.authenticated:
    batch_size = 100

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

    batch_generator = get_data_generator(st.session_state.dataset)
    batches = list(batch_generator)  # Collect all batches into a list (for pagination)
    num_batches = len(batches)

    # Ensure session state for batch_index and record_index
    if "batch_index" not in st.session_state:
        st.session_state.batch_index = 0
    if "current_record_index" not in st.session_state:
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
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Next"):
            # Increment the current_record_index and possibly batch_index
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

    with col2:
        if st.button("Random"):
            # Randomly select a batch and record within the valid range
            random_batch_index = random.randint(0, num_batches - 1)
            random_record_index = random.randint(0, len(batches[random_batch_index]) - 1)

            # Update the session state with the random values
            st.session_state.batch_index = random_batch_index
            st.session_state.current_record_index = random_record_index

            # Get the selected batch and record for the normal view
    batch = batches[st.session_state.batch_index]
    selected_record = batch.iloc[st.session_state.current_record_index]

    # Display the selected conversation
    st.write(f"Currently Viewing: Batch {st.session_state.batch_index}, Record {st.session_state.current_record_index}")

    id = selected_record.get("id")
    st.subheader(f"ID: {id}")
    st.subheader("Conversation:")
    display_conversation(selected_record)
