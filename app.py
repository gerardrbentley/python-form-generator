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
        st.code(model_code)


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
