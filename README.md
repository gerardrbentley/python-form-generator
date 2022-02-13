# Python Form Generator

From raw JSON to Python Pydantic Model to Streamlit Input Form :exploding_head:

Bootstrapping more Streamlit apps from within a Streamlit app :recycle:

Generate well-typed and validated Python forms from basic JSON example.

*DEPENDENCIES:*
- [Datamodel Code Generator](https://github.com/koxudaxi/datamodel-code-generator/) for mapping to Pydantic model
- [JSON to Pydantic](https://jsontopydantic.com/) for proof this can work
- [Streamlit Pydantic](https://github.com/LukasMasuch/streamlit-pydantic) for bootstrapped app code

## Full Walkthrough

### Skeleton

*GOAL:*
Initialize git repo with necessary file scaffold:

- `app.py`: The main streamlit entry app
- `requirements.txt`: Pin versions of Python packages so deployment and development is repeatable
- `README.md`: This documentation
- `.gitignore`: Prevent secrets or large files or unecessary things from going into github
    - Recommended github python [gitignore template](https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore) works fine for this, slightly overkill
- `LICENSE`: [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) same as [Streamlit Terms](https://streamlit.io/terms-of-use)

```sh
mkdir python-form-generator
cd python-form-generator/
touch README.md LICENSE .gitignore app.py requirements.txt
git init
git checkout -b main
git remote add origin git@github.com:gerardrbentley/python-form-generator.git
git add .
git commit -m "skeleton"
```

### Install

We'll plan on 4 main packages for this:

- `streamlit`
- `pydantic`
- `streamlit-pydantic`
- `datamodel-code-generator`

```sh
python -m venv venv
. ./venv/bin/activate
pip install streamlit-pydantic datamodel-code-generator
pip list | grep "streamlit\|pydantic\|datamodel-code"
```

*Note:* This lets `streamlit-pydantic` to choose which versions of `streamlit` and `pydantic` work for the latest release.

Saving the output to `requirements.txt` in the format:

```txt
datamodel-code-generator==0.11.19
pydantic==1.9.0
streamlit==1.5.1
streamlit-pydantic==0.5.0
```

Saving the output to requirements.txt allows new users / deploys to install pinned verions with something like the following:

`pip install -r requirements.txt`

```sh
git add requirements.txt README.md
git commit -m "install"
```

### Hello World

Adding the following to `app.py`:

```py
import streamlit as st


def main() -> None:
    st.header("Python Form Generator")
    st.subheader("Enter your JSON and get a free Pydantic model + Streamlit Input Form using it!")
    json_input = st.text_area('JSON example', height=200)
    st.write(json_input)


if __name__ == "__main__":
    main()
```

Then run with `streamlit` to check if basic input / processing frontend works.

```sh
streamlit run app.py
# ctrl + c to stop
```

```sh
git add app.py README.md
git commit -m "input hello world"
```

### Model Generation

We'll draw from 3 sources for the meat and potatoes of this app:

- [Streamlit Pydantic Usage Guide](https://github.com/LukasMasuch/streamlit-pydantic#usage)
- [Datamodel Code Generator conversion](https://github.com/koxudaxi/datamodel-code-generator/blob/381abc1946c088c99dc79bebc62b7e37a2d4b8d3/datamodel_code_generator/__init__.py#L311)
- [JSON to Pydantic conversion](https://github.com/brokenloop/jsontopydantic/blob/master/server/app/scripts/generator.py)

#### Imports

Expand import section of `app.py` to accomodate Streamlit Pydantic, Datamodel code generator, and GenSON

(Datamodel code generator is intended as CLI tool, so we have to dig a bit into it)

```py
import json

from pydantic import Json, BaseModel
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser
from genson import SchemaBuilder
import streamlit as st
import streamlit_pydantic as sp
```

#### Upgraded Input

We'll use Streamlit Pydantic to get out of the box validation of the JSON that the user provides. 
Plus we get extensibility via the FormModel if we want to add more configuration options!

Instead of a plain `text_input` from streamlit, we utilize `sp.pydantic_form` and provide our model (which only has 1 input field for now!)

After getting some input JSON from the User it will pass off to converting to a model.

```py
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
```

#### Conversion

Following in the footsteps of JSON to Pydantic and Datamodel Code Generator, we use GenSON to build a JSONSchema representation from raw JSON data, then dump that into the Datamodel Code Generator parser.

We'll handle the same error case Datamodel code generator does, otherwise assume the happy path and display the results!

```py
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
```

#### LGTM

Trying out a simple entry (even simpler than the [littlest fullstack app](https://streamlit-postgres.gerardbentley.com/)) such as the following:

```txt
{"body": ":tada:", "username": ":cat:"}
```

Produces expected result

```py
from __future__ import annotations

from pydantic import BaseModel


class Model(BaseModel):
    body: str
    username: str
```

Time to ship it and generate a Form!

```sh
git add app.py README.md
git commit -m "model generation"
```

### Bootstrapping

Alright, we've got a nice Pydantic model, time to generate a Streamlit Pydantic scaffold from it and provide a download link.

#### Update Show Model

We'll allow the user to download just the model into a `.py` file and hide the generated model unless they want to see it.

```py
def show_generated_code(schema: Json) -> None:
    model_code = json_to_pydantic(schema)

    if not model_code:
        st.error("Models not found in the input data")
    else:
        with st.expander("Original Converted Model"):
            st.code(model_code, language="python")
        st.download_button("Download Generated Model Only", data=model_code, file_name="model.py", mime="text/plain")
        show_generated_form(model_code)
```

#### Inject Generated Code

We only need 2 features to really bootstrap these forms:

- Added imports
- Retrieve form data in Streamlit app

I'll add a `main()` method to keep scope contained, but the Streamlit execution model embraces all [Python scripting](https://streamlit.io/)

```py
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
```

#### LGTM

Testing out the download and run on our simple model yields great results!

```sh
git add app.py README.md
git commit -m "app generation"
```

### Wrap Up

That's it for the basic idea!

Next steps would be allowing configuration options such as "all Optional" and snake casing akin to JSON to Pydantic.
Also more input forms, as Datamodel code generator handles OpenAPI, CSV data, and more.

```sh
git add README.md
git commit -m "lgtm!"
git push origin main
```