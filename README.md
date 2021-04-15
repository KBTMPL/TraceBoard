# TraceBoard

Simple dashboard for setting up and viewing traces

- Bash for backend
- CherryPy python3 web framework for frontend

Dependencies:

- mtr
- traceroute
- hping3
- proper rights for raw sockets
- jq
- other bash cmds
- python3 (cherrypy, os, csv, datetime, re modules)

Example usage:

```
./schedule_trace.sh --binary='mtr' --end_stamp=`echo $(date "+%s") + 900|bc` --interval=5  --proto=tcp  --dst_port=443  --psize=1460 --count=30 --target=www.disney.com
```
