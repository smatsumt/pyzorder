test:
	python3 -m unittest discover tests

dist:
	python3 setup.py sdist

release-test: dist
	twine upload --repository testpypi dist/*

release: dist
	twine testpypi dist/*

clean:
	rm -rf dist *.egg-info
