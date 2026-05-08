.PHONY: build check test bump clean

build:
	python -m scripts.build

check:
	python -m scripts.check

test:
	pytest -v

# Update the upstream SHA pin in manifest.yaml, then rebuild + recheck.
# Usage: make bump SHA=<new-sha>
bump:
	@test -n "$(SHA)" || (echo "ERROR: pass SHA=<new-sha>" >&2; exit 1)
	sed -i.bak -E 's/^( {2}commit: ).*/\1$(SHA)/' manifest.yaml
	rm manifest.yaml.bak
	$(MAKE) build
	$(MAKE) check

clean:
	rm -rf COMPANY.md teams/ agents/ skills/ images/
