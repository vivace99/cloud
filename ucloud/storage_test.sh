#!/bin/bash
  
url=https://ssproxy.ucloudbiz.olleh.com/auth/v1.0

for S in `seq 1 $1` 
do
	echo $S
	curl -X GET -v -i -H 'X-Storage-User: dessert@c2dgames.com' -H 'X-Storage-Pass: MTM4NDMxMDc3NTEzODQzMDc0MzE2NjYw' $url 
done
