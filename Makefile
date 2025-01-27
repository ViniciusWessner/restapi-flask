APP = restapi

test:
	# @flake8 . --exclude venv application

compose: test
	@docker compose build
	@docker compose up

run:
	@docker compose up
