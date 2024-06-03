# Define the Python executable to use
PYTHON = poetry run python

# Default target to show help
.DEFAULT_GOAL := help

# Target to show help
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Target to install dependencies
install:  ## Install dependencies
	poetry install

# Target to run the Django server
run:  ## Run the Django development server
	$(PYTHON) manage.py runserver

# Target to run migrations
migrate:  ## Run database migrations
	$(PYTHON) manage.py migrate

# Target to create migrations
makemigrations:  ## Create new database migrations
	$(PYTHON) manage.py makemigrations

# # Target to run tests
# test:  ## Run tests
# 	poetry run pytest
