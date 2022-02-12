import streamlit as st


def main() -> None:
    st.header("Python Form Generator")
    st.subheader("Enter your JSON and get a free Pydantic model + Streamlit Input Form using it!")
    json_input = st.text_area('JSON example', height=200)
    st.write(json_input)


if __name__ == "__main__":
    main()