# network_delay

Python script for monitoring connectivity delay between hosts.

Need to create a logs directory in the directory where the script is located.
```
$ mkdir logs
```
Script execution mode:

Usage: network_delay.py host [port] [maxCount]

Example:
```
./network_delay.py darkstar 10000 10
```
Log output format:
```
2022-10-14 12:16:11,703 - PID=1093440 - INFO - TCP Ping Results for myhost: Connections (Total/Pass/Fail): [10/10/0] (Failed: 0%)
2022-10-14 12:18:02,199 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=0 time=21.79 ms
2022-10-14 12:18:03,462 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=1 time=261.68 ms
2022-10-14 12:18:04,491 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=2 time=28.25 ms
2022-10-14 12:18:05,512 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=3 time=19.28 ms
2022-10-14 12:18:06,534 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=4 time=20.62 ms
2022-10-14 12:18:07,572 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=5 time=37.52 ms
2022-10-14 12:18:08,622 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=6 time=41.41 ms
2022-10-14 12:18:10,439 - PID=1099039 - INFO - Connected to darkstar[10000]: tcp_seq=7 time=814.63 ms
```
