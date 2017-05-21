all: test test_clean
test:
	CERTBOT_INWX_HOOK_CONFIG_FILE=certbot_inwx_hook/test.ini python -c "from certbot_inwx_hook.main import deploy; deploy()"
test_clean:
	CERTBOT_INWX_HOOK_CONFIG_FILE=certbot_inwx_hook/test.ini python -c "from certbot_inwx_hook.main import cleanup; cleanup()"

build: clean
	python setup.py sdist bdist_wheel

upload: clean build
	twine upload -s -i faerbit@gmail.com  dist/*

clean:
	rm -rf build dist *.egg-info
