import json

from pydantic import Json, BaseModel
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from genson import SchemaBuilder
import streamlit as st
import streamlit_pydantic as sp


class FormGeneratorModel(BaseModel):
    model_schema: Json


def main() -> None:
    st.header("Python Form Generator")
    st.subheader(
        "Enter your JSON and get a free Pydantic model + Streamlit Input Form using it!"
    )
    data = sp.pydantic_form(key="json_input", model=FormGeneratorModel)
    if data:
        show_generated_code(data.model_schema)


def show_generated_code(schema: Json) -> None:
    model_code = json_to_pydantic(schema)

    if not model_code:
        st.error("Models not found in the input data")
    else:
        with st.expander("Original Converted Model"):
            st.code(model_code, language="python")
        st.download_button("Download Generated Model Only", data=model_code, file_name="model.py", mime="text/plain")
        show_generated_form(model_code)

MAIN_TEMPLATE = """\


def main() -> None:
    st.header("Model Form Submission")
    data = sp.pydantic_form(key="my_model", model=Model)
    if data:
        st.json(data.json())


if __name__ == "__main__":
    main()
"""

def show_generated_form(model_code: str) -> None:
    code_lines = model_code.split('\n')
    code_lines.insert(2, "import streamlit_pydantic as sp")
    code_lines.insert(2, "import streamlit as st")

    code_lines.insert(-1, MAIN_TEMPLATE)

    full_code = '\n'.join(code_lines)

    st.subheader("Generated Streamlit Pydantic App")
    st.caption("Download it and run with `streamlit run model_form.py`")
    st.download_button("Download Generated Form!", data=full_code, file_name="model_form.py", mime="text/plain")
    st.code(full_code, language="python")


def json_to_pydantic(input_text: str) -> str:
    builder = SchemaBuilder()
    builder.add_object(input_text)
    schema = builder.to_schema()
    parser = JsonSchemaParser(
        source=json.dumps(schema),
        base_class="pydantic.BaseModel",
    )

    return parser.parse()


if __name__ == "__main__":
    main()
