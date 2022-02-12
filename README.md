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