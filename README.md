# TraceBoard

Simple dashboard for setting up and viewing traces

- Bash for backend
- Most likely lightweight python web framework for frontend

Dependencies:

- mtr
- traceroute
- hping3
- proper rights for raw sockets
- jq
- other bash cmds

Example usage:

```
./schedule_trace.sh --binary='mtr' --end_stamp=`echo $(date "+%s") + 900|bc` --interval=5  --proto=tcp  --dst_port=443  --psize=1460 --count=30 --target=www.disney.com
```
