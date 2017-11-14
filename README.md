# mastermindg/docker-flexget

Read all about FlexGet [here](http://www.flexget.com/#Description).

This fork shows an example of a modular config where all the values come from environment variables. It's a basic config for now but will be expanded to encompass all of the available options. It's using transmission as the plugin for now.

## Usage

```
docker create \
    --name=flexget \
    -e WEBSERVER=yes \
    -e INTERVAL=5 \
    -e RSS="https://www.myrssfeed.com" \
    -e TRANSMISSION_HOST="transmission" \
    -e TRANSMISSION_PORT="9091" \
    -e TRANSMISSION_USER="admin" \
    -e TRANSMISSION_PASS="admin" \
    -e PGID=<gid> -e PUID=<uid> \
    -e WEB_PASSWD=yourhorriblesecret \
    -e TORRENT_PLUGIN=transmission \
    -e FLEXGET_LOG_LEVEL=debug \
    -p 5050:5050 \
    -v <path to downloads>:/downloads \
    mastermindg/docker-flexget
```

This container is based on phusion-baseimage with ssh removed. For shell access whilst the container is running do `docker exec -it flexget /bin/bash`.

**Parameters**

* `-e WEBSERVER` for the option to run the webserver
* `-e INTERVAL` for the interval for check the RSS feed
* `-e RSS` for the path to the rss feed
* `-e TRANSMISSION_HOST` for the transmission host
* `-e TRANSMISSION_PORT` for the transmission port
* `-e TRANSMISSION_USER` for the transmission user
* `-e TRANSMISSION_PASS` for the transmission password
* `-e PGID` for GroupID - see below for explanation
* `-e PUID` for UserID - see below for explanation
* `-e WEB_PASSWD` for the Web UI password - see below for explanation
* `-e TORRENT_PLUGIN` for the torrent plugin you need, e.g. "transmission" or "deluge"
* `-e FLEXGET_LOG_LEVEL` for logging level - see below for explanation
* `-p 5050` for Web UI port - see below for explanation
* `-v /downloads` - location of downloads on disk


**Torrent plugin: Transmission**

FlexGet is able to connect with transmission using `transmissionrpc`, which is installed as the default torrent plugin in this container. For more details, see http://flexget.com/wiki/Plugins/transmission.

Please note: This Docker image does NOT run Transmission. Consider running a [Transmission Docker image](https://github.com/linuxserver/docker-transmission/) alongside this one.

For transmission to work you can either omit the `TORRENT_PLUGIN` environment variable or set it to "transmission".

**Torrent plugin: Deluge**

FlexGet is also able to connect with deluge using `deluge-common`, which can be installed in this container, replacing the transmission plugin. For more details, see https://www.flexget.com/Plugins/deluge.

Please note: This Docker image does NOT run Deluge. Consider running a [Deluge Docker image](https://hub.docker.com/r/linuxserver/deluge/) alongside this one.

For deluge to work you need to set `TORRENT_PLUGIN` environment variable to "deluge".

**Daemon mode**

This container runs flexget in [daemon mode](https://flexget.com/Daemon). This means by default it will run your configured tasks every hour after you've started it for the first time. If you want to run your tasks on the hour or at a different time, look at the [scheduler](https://flexget.com/Plugins/Daemon/scheduler) plugin for configuration options. Configuration is automatically reloaded every time just before starting the tasks as scheduled, to apply your changes immediately you will need to restart the container.

**Web UI**

FlexGet is able to host a Web UI if you have this enabled in your configuration file. See [the wiki](https://flexget.com/wiki/Web-UI) for all details. To get started, simply add:

```
web_server: yes
```

The Web UI is protected by a login, you need to either set the `WEB_PASSWD` environment variable or setup a user after starting this docker:

Connect with the running docker:

```
docker exec -it flexget bash
```

If your configuration file is named "config.yml" you can setup a password like this:

```
flexget -c /config/config.yml web passwd <some_password>
```

Now you can open the Web UI at `http://<ip-of-the-machine-running-docker>:5050` and login with this password, use `flexget` as your username.

Note: if you ever change your password in a running container, don't worry. Recreating or restarting your container will not simply overwrite your new password. If you want to reset your password to the value in `WEB_PASSWD` you can simply remove the `.password-lock` file in your config folder.

**Logging Level**

Set the verbosity of the logger. Optional, defaults to debug if not set. Levels: critical, error, warning, info, verbose, debug, trace.

### User / Group Identifiers

**TL;DR** - The `PGID` and `PUID` values set the user / group you'd like your container to 'run as' to the host OS. This can be a user you've created or even root (not recommended).

Part of what makes this container work so well is by allowing you to specify your own `PUID` and `PGID`. This avoids nasty permissions errors with relation to data volumes (`-v` flags). When an application is installed on the host OS it is normally added to the common group called users, Docker apps due to the nature of the technology can't be added to this group. So this feature was added to let you easily choose when running your containers.

[Flexget CLI](https://flexget.com/CLI)

## Updates / Monitoring

* Upgrade to the latest version of FlexGet simply `docker restart flexget`.
* Monitor the logs of the container in realtime `docker logs -f flexget`.

**Credits**
* [linuxserver.io](https://github.com/linuxserver) for providing awesome docker containers.
