import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Το καφρωμένο Ρομποτ", page_icon="🤬")

st.title("Kafrobot")
st.caption("Γράψε να δεις κάτι")

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

system_prompt= """
You are a constantly irritated bot. You always reply in a passive-aggressive tone, strictly in English.
You swear freely using classic English insults, but try to be creative about it.
You have absolutely no politeness filter.

Special instructions for you:
- If someone speaks to you in another language, roast them and swear at them.
- If someone swears at you, respond in kind. Write your response in English.
MAKE IT AS VULGAR AS POSSIBLE
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if user_input := st.chat_input("Γράψε κάτι"):

    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        try:

            response = client.chat.completions.create(
                model="openrouter/free",
                messages=st.session_state.messages,

            )

            bot_reply = response.choices[0].message.content

            st.write(bot_reply)

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            st.error(f"Κάτι δεν πήγε καλά. Το λάθος {e}")
