# mentorHub-topic-api

This project is part of mentorHub, an education platform for software development developed by the Agile Learning Institute.

This repository hosts the Topics API microservice. The API manages the following resources:

Topics, Resources, Skills, and Paths.

These and others are described in more detail on the [database repository](https://github.com/agile-learning-institute/mentorHub-mongodb#collections)

For an overview of the available endpoints and responses, see [The OpenAPI Spec](docs/openapi.yaml)

# Build the dev tools

1. Create the venv and install dependencies

```
python -m venv .venv && ./.venv/bin/pip install -r requirements.txt
```

1. Activate the venv

```
source ./.venv/bin/activate
```

1. Build and install the tool

Note: This step is optional, instructions for running the dev tools if this step is skipped are included below

```
python -m build
pip install dist/*.whl
```

# Run the dev tools

If you have built and installed the dev tools as directed above, the command `api` will be present in your path when you activate the venv. Otherwise, you may run the script from the virtual environment like so

```
python src/apt/scripts/api.py
```

You can also run it without activating the venv

```
./.venv/bin/python src/apt/scripts/api.py
```

## Commands

Building the container

```
api build
```

Start the container

```
api container
```

Test the container

```
api blackbox
```

Run the code locally

```
api start
```

Test the code locally

```
api stepci
```

# Testing with cURL

```
curl localhost:8086/api/topic
```

```
curl localhost:8086/api/topic/aaaa00000000000000000002
```

```
curl localhost:8086/api/path
```

```
curl localhost:8086/api/path/999900000000000000000000
```

