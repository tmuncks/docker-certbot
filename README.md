## Certbot docker container

With certbot-dns-powerdns plugin that supports PowerDNS-Admin

Git repository: https://github.com/tmuncks/docker-certbot/

### How it works

Parameters to `certbot` can be passed as the command to the container, just like the original `certbot/certbot` image.

### Oneshot mode

The default is to run `certbot` once and exit. This **oneshot** mode works exactly like the original `certbot/certbot` image.

### Automatic renewal

Sometimes it is useful to leave the container running after certificate generation, and automatically handle renewals on regular intervals as well.

We can disable **oneshot** mode by setting the `CERTBOT_ONESHOT` environment variable to `0`.

This will still cause the image to run `certbot` on start, but it will not exit. Instead, it will repeat the `certbot` command every night at 03:00, indefinitely.

### PowerDNS integration

Parameters to the dns-powerdns authenticator plugin, can be specified by
setting the `DNS_POWERDNS_API_URL` and `DNS_POWERDNS_API_KEY` environment
variables.

They can also be passed as a mounted `pdns-credentials.ini` file,
containing the `dns-powerdns-api-url` and `dns-powerdns-api-key` options,
as documented for [certbot-dns-powerdns](https://github.com/tmuncks/certbot-dns-powerdns).

### Environment variables
|ENV|Description|
|---|-----------|
|`CERTBOT_ONESHOT`|Set to 0 to automatically rerun certbot every night at 03:00|
|`DNS_POWERDNS_API_URL`|Specify value for --dns-powerdns-api-url|
|`DNS_POWERDNS_API_KEY`|Specify value for --dns-powerdns-api-key|

### Examples

An example `docker-compose.yml` can be found under the `compose` directory in the repo.