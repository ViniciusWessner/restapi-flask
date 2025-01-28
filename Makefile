APP = restapi

test:
	@flake8 . --exclude venv

compose: test
	@pip freeze > requirements.txt
	@docker compose build
	@docker compose up

run:
	@docker compose up
