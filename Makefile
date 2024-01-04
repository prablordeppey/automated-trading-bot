# Makefile

# Help target (displays help comments for each target)
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk '/^# target:/ {sub(/^# target: /, "\t"); gsub(/##/, ":"); print}' $(MAKEFILE_LIST)

# target: setup_dev_env ## Setup the development environment
init_dev_env: install_core_libs init_virtual_env export_requirements
	poetry install

install_core_libs:
	pip install poetry

init_virtual_env:
	# install virtualenvs
	pip install virtualenv
	# create virtualenv
	virtualenv venv

# target: export_requirements ## Exports prod/dev requirement files
export_requirements:
	rm -f requirements/prod.txt requirements/dev.txt
	mkdir -p requirements
	poetry export --format requirements.txt > requirements/prod.txt --without-hashes
	poetry export --format requirements.txt > requirements/dev.txt --dev --without-hashes

# target: update_dev_env ## Update locked dependencies when Pyproject.toml changes
update_dev_env:
	poetry lock
	pip install poetry

# target: package_app ## Packages the application
package_app:
	poetry build -vvv -n

# target: run-app ## Runs the application
run-app:
	poetry run python -m bot

# target: run_linter ## Checks code integrity
check_linter:
	poetry run ruff check .

# target: fix_linter ## Checks code integrity
fix_linter:
	poetry run ruff check . --fix
