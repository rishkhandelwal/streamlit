import streamlit as st
import requests
import json
from datetime import datetime

def send_message(api_url, user_id, user_input):
    try:
        response = requests.post(
            api_url,
            json={'user_id': user_id, 'user_input': user_input}
        )
        response.raise_for_status()
        
        data = response.json()
        
        if 'response' in data:
            if isinstance(data['response'], list):
                return " ".join(data['response'])
            elif isinstance(data['response'], str):
                return data['response']
            else:
                return f"Unexpected response format: {type(data['response'])}"
        else:
            return f"No 'response' key in API response. Keys found: {', '.join(data.keys())}"
    except requests.RequestException as e:
        return f"API request error: {str(e)}"
    except json.JSONDecodeError:
        return f"Failed to parse JSON response. Raw response: {response.text}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def fetch_chat_history(api_url, user_id):
    try:
        response = requests.get(f"{api_url}/history/{user_id}")
        response.raise_for_status()
        return response.json().get('chat_history', [])
    except requests.RequestException as e:
        st.error(f"Failed to fetch chat history: {str(e)}")
        return []

def main():
    st.title("Chatbot App with Chat History")
    
    user_id = st.text_input("Enter your User ID:")
    
    if user_id:
        if 'user_id' not in st.session_state or st.session_state.user_id != user_id:
            st.session_state.user_id = user_id
            # Fetch chat history when user ID is entered or changed
            chat_history = fetch_chat_history("https://v-friend-anjali-ov26lo32lq-el.a.run.app/api", user_id)
            st.session_state.messages = [(msg['sender'], msg['message']) for msg in chat_history]
        
        st.write("### Chat with Anjali")
        
        for sender, msg in st.session_state.messages:
            with st.chat_message(sender.lower()):
                st.write(msg)
        
        user_input = st.chat_input("Your message:")
        
        if user_input:
            st.session_state.messages.append(("User", user_input))
            bot_response = send_message("https://v-friend-anjali-ov26lo32lq-el.a.run.app/api/manager-chat=2", user_id, user_input)
            st.session_state.messages.append(("Anjali", bot_response))
            st.experimental_rerun()

if __name__ == "__main__":
    main()