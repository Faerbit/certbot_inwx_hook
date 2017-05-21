# certbot INWX hook [![PyPI version](https://badge.fury.io/py/certbot-inwx-hook.svg)](https://badge.fury.io/py/certbot-inwx-hook)

A hook to be used with the `--manual` option of the `certonly` subcommand of
certbot. The hooks work with the API of [INWX](https://inwx.com) and the
`dns-01` challenge of [Let's encrypt](https://lets-encrypt.org).

## Usage
This package installs the `certbot_inwx_deploy` and `certbot_inwx_cleanup`
entry points. Just supply these to the `--manual-auth-hook` and
`--manual-cleanup-hook` of certbot.

## Configuration
The configuration file is stored under `/etc/certbot_inwx_hook.ini`. A sample
is provided under `/etc/certbot_iwnx_hook.sample.ini`. You can set the
`$CERTBOT_INWX_HOOK_CONFIG_FILE` environment variable to a custom location,
which will take precedence over the default location if set.
In the config file you have to supply your login information. Optionally you
can set additioanl nameserver IPs to check for successful propagation of the
challenge. You would want ot provide the IPs of your registrar here to speed
things up.

## License
This work is licensed under the MIT license. See License.md for details.
Additionally this work is loosely based on
[this](https://github.com/inwx/python2.7-client) code.
