clean-build-env:
	$(shell [ -d *.egg-info ] && rm -r simple_repr.egg-info/)
	$(shell [ -d dist ] && rm -r dist/)
	$(shell [ -d build ] && rm -r build/)

	@echo "Cleaned up build environment."

build-lib:
	@echo "Building lib..."
	python setup.py sdist bdist_wheel
	twine check dist/*

deploy:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

deploy-live:
	twine upload dist/*
