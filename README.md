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