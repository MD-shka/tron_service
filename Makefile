.PHONY: run test precommit

# Запуск приложения. Если основная точка входа находится в модуле app.main
run:
	python -m app.main

# Запуск тестов с помощью pytest
test:
	pytest

# Прогон прекоммит проверок с помощью pre-commit
precommit:
	pre-commit run --all-files

