.PHONY: dev
dev:
	@tox -e pre-commit -- install -f --install-hooks
