# mentorHub-topic-api

This project is part of mentorHub, an education platform for software development developed by the Agile Learning Institute.

This repository hosts the Topics API microservice. The API manages the following resources:

Topics, Resources, Skills, and Paths.

These and others are described in more detail on the [database repository](https://github.com/agile-learning-institute/mentorHub-mongodb#collections)

For an overview of the available endpoints and responses, see [The OpenAPI Spec](docs/openapi.yaml)

# To build the tool

Create the venv and install dependencies

```
python -m venv .venv && ./.venv/bin/pip install -r requirements.txt
```

Activate the venv

```
source ./.venv/bin/activate
```

Build the tool

```
python -m build
```

Install it

```
pip install dist/*.whl
```

# Run it

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

