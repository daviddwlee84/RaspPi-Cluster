```bash
$ docker compose -f docker-compose.openpbs.auto.yml up
Attaching to pbs-c1, pbs-c2, pbs-head, pbs-init
pbs-head  | Starting PBS
pbs-c1    | Starting PBS
pbs-c2    | Starting PBS
pbs-head  | PBS Home directory /var/spool/pbs needs updating.
pbs-head  | Running /opt/pbs/libexec/pbs_habitat to update it.
pbs-init  | /bin/bash: /init/pbs-init.sh: /usr/bin/env: bad interpreter: Permission denied
pbs-c1    | PBS Home directory /var/spool/pbs needs updating.
pbs-c1    | Running /opt/pbs/libexec/pbs_habitat to update it.
pbs-head  | ***
pbs-c2    | PBS Home directory /var/spool/pbs needs updating.
pbs-c2    | Running /opt/pbs/libexec/pbs_habitat to update it.
pbs-c1    | ***
pbs-c2    | ***
pbs-init exited with code 126
pbs-c2    | /opt/pbs/sbin/pbs_dataservice: line 218: echo: write error: Permission denied
pbs-head  | /opt/pbs/sbin/pbs_dataservice: line 218: echo: write error: Permission denied
pbs-c1    | /opt/pbs/sbin/pbs_dataservice: line 218: echo: write error: Permission denied
pbs-c2    | pg_ctl: another server might be running; trying to start server anyway
pbs-head  | pg_ctl: another server might be running; trying to start server anyway
pbs-c1    | pg_ctl: another server might be running; trying to start server anyway
pbs-c2    | *** End of /opt/pbs/libexec/pbs_habitat
pbs-c1    | *** End of /opt/pbs/libexec/pbs_habitat
pbs-c2    | Home directory /var/spool/pbs updated.
pbs-c1    | Home directory /var/spool/pbs updated.
pbs-head  | *** End of /opt/pbs/libexec/pbs_habitat
pbs-head  | Home directory /var/spool/pbs updated.
pbs-c2    | /opt/pbs/sbin/pbs_comm ready (pid=513), Proxy Name:pbs-c2:17001, Threads:4
pbs-c1    | /opt/pbs/sbin/pbs_comm ready (pid=513), Proxy Name:pbs-c1:17001, Threads:4
pbs-c1    | PBS comm
pbs-c2    | PBS comm
pbs-head  | /opt/pbs/sbin/pbs_comm ready (pid=513), Proxy Name:pbs-head:17001, Threads:4
pbs-head  | PBS comm
pbs-head  | Creating usage database for fairshare.
pbs-head  | PBS sched
pbs-c2    | PBS mom
pbs-c1    | PBS mom
pbs-c2    | Creating usage database for fairshare.
pbs-c1    | Creating usage database for fairshare.
pbs-c2    | PBS sched
pbs-c1    | PBS sched
pbs-head  | Connecting to PBS dataservice......continuing in background.
pbs-head  | PBS server
pbs-c1    | Connecting to PBS dataservice......continuing in background.
pbs-c1    | PBS server
pbs-c2    | Connecting to PBS dataservice......continuing in background.
pbs-c2    | PBS server
```

> BUG: failed to init
