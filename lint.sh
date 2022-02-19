isort --profile black taocp
black taocp
flake8 taocp --max-line-length 88
mypy --strict taocp
