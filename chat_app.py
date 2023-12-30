from queue import Queue
from threading import Thread;
import numpy as np;
import pandas as pd;
import streamlit as st;
import atexit
import logging;
import json;

if __name__ == '__main__':
    # Function to be called before exiting
    def exit_app_handler():
        logging.info("Application is ending!");

atexit.register(exit_app_handler);
st.title("StackOverflow for Programmers-Chat App-For Programmers and Related Topics!");

st.markdown("Ask Programming Related Topics and Other Non Programming Questions ");


with st.chat_message("user"):
    st.write("Hello")