import streamlit as st

class AssistantUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages
        self.employee_information = assistant.employee_information

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        messages = self.messages

        for message in messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            if message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def set_state(self, key, value):
        st.session_state[key] = value

    def render_user_input(self):
        user_input = st.chat_input("Type here...", key="input")
        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)

            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})

            self.set_state("messages", self.messages)

    def render(self):
        with st.sidebar:
            st.logo(
                "https://media.istockphoto.com/id/1450261341/vector/careergrowth-hadshake-black-icon.jpg?s=612x612&w=0&k=20&c=WuXetiJpwhJUvM2D9n7h6cByAtXvpYWg3j0DQc-g-8M="
            )
            st.title("Sherpa AI Assistant")

            st.subheader("Client Information")
            st.write(self.employee_information)

        self.render_messages()

        self.render_user_input()

    