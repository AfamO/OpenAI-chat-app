import numpy as np;
import streamlit as st;
import atexit
import logging;
import random;
import time;
import openai;
from PIL import Image;
from flask import Flask, redirect, render_template, request, url_for
import pandas;
from openai.error import RateLimitError, APIConnectionError,AuthenticationError

if __name__ == '__main__':
    # Function to be called before exiting
    def exit_app_handler():
        logging.info("Application is ending!");

atexit.register(exit_app_handler);
# Exhausted Api Rate Limit Simulate random manual bot responses for EXHAUSTED RATE LIMIT COMPLAINT BY OPEN AI
assitant_responses = random.choice(
        [
            "Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile",
            "JAVA was developed by James Gosling at Sun Microsystems Inc in the year 1995, later acquired by Oracle Corporation. It is a simple programming language. Java makes writing, compiling, and debugging programming easy. It helps to create reusable code a.",
            "Java was first released in 1995 and is widely used for developing applications for desktop, web, and mobile devices. Java is known for its simplicity, robustness, and security features, making it a popular choice for enterprise-level applications.",
            "As a simple programming language. Java makes writing, compiling, and debugging programming easy. It helps to create reusable code and modular programs.",
            "Java is a class-based, object-oriented programming language and is designed to have as few implementation dependencies as possible.",
            "A general-purpose programming language made for developers to write once run anywhere that is compiled Java code can run on all platforms that support Java. Java applications are compiled to byte code that can run on any Java Virtual Machine. The syntax of Java is similar to c/c++."
        ]
    );

#OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"];

image = Image.open('stackoverflow.jpg');
st.image(image, caption='Image Credit:stackoverflow.com', width=500)
st.title("Bolt for Programmers!");
st.markdown("Ask Programming Related Questions and Other Non Programming Questions ");
st.divider();

def generate_response(is_chatgpt=True):
    message_placeholder = st.empty();
    full_response = "";
    try:
        for chatgpt_responses in openai.Completion.create(
                model="text-davinci-003",
                messages=[{"role": msg['role'], "content": msg["content"]} for msg in st.session_state.messages],
                stream=True,
        ):
            full_response += chatgpt_responses.choices[0].delta.get("content", "");
            message_placeholder.markdown(full_response + "  ");
    except RateLimitError:
        logging.info("Rate Limit Exceeded! Navigating to offline/manual bolt responses")
        for chunk in assitant_responses.split():
            full_response += chunk+" ";
            time.sleep(0.05)
            message_placeholder.markdown(full_response);
    except APIConnectionError:
        logging.info("APIConnection/Internet Error! Navigating to offline/manual bolt responses")
        for chunk in assitant_responses.split():
            full_response += chunk + " ";
            time.sleep(0.05)
            message_placeholder.markdown(full_response);
    except AuthenticationError:
        logging.info("Authentication(API Key) Error! Navigating to offline/manual bolt responses")
        for chunk in assitant_responses.split():
            full_response += chunk + " ";
            time.sleep(0.05)
            message_placeholder.markdown(full_response);
    message_placeholder.markdown(full_response);
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response});


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})


    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        generate_response(True);