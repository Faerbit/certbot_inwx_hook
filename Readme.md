# certbot INWX hook

A hook to be used with the `--manual` option of the `certonly` subcommand of
certbot. The hooks work with the API of [INWX](https://inwx.com) and the
`dns-01` challenge of [Let's encrypt](https://lets-encrypt.org).

## Usage
This package installs the `certbot_inwx_deploy` and `certbot_inwx_cleanup`
entry points. Just supply these to the `--manual-auth-hook` and
`--manual-cleanup-hook` of certbot.
Additionally the deploy hook will clean up after itself after 3 minutes.

## Configuration
The configuration file is stored under `/etc/certbot_inwx_hook.ini`. You can
set the `$CERTBOT_INWX_HOOK_CONFIG_FILE` environment variable to a custom
location, which will take precedence over the default location if set.
In the config file you have to supply your login information.
Additionally you can set nameserver IPs to check for successful propagation of
the challenge.

## License
This work is licensed under the MIT license. See License.md for details.
Additionally this work is loosely based on
[this](https://github.com/inwx/python2.7-client) code.
