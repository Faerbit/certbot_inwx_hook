test:
	CERTBOT_INWX_HOOK_CONFIG_FILE=certbot_inwx_hook/test.ini python -c "from certbot_inwx_hook.main import deploy; deploy()"
