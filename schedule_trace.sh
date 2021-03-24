#!/bin/bash
#rewrite exit flags to ghost like

#init
source init.sh;
exec_date=`date +%s`;
ef="0";

#miscellany
BLUE='\033[0;34m';
GREEN='\033[0;32m';
RED='\033[0;31m';
NC='\033[0m';

#test mode info
if [ "$prod" == "0" ] ; then
        echo -e "${GREEN}running in test mode no actions are actually done\n${NC}";
	echo -e "${BLUE}check \$? variable to see the output code of script\n${NC}";
	if [[ $# -eq 0 ]] ; then
		echo -e "${RED}I see you did not provide any args and running in test mode grab this sample command:\n${NC}";
		echo  './schedule_trace.sh mtr ` echo $(date "+%s") + 7201|bc` 15 icmp 1337 2137 1460 100 onet.pl'
	fi
fi

#params
binary=$1;      #mtr hping3 traceroute
end_stamp=$2;   #timestamp in epoch format for when job should end
interval=$3;    #value in minutes 5, 10, 15, 30 or 60
proto=$4;       #tcp udp icmp
src_port=$5;    #source port (if applicable)
dst_port=$6;    #destination port (if applicable)
psize=$7;       #packet size in bytes
count=$8;       #number of probes to be sent
target=$9;      #destination for the trace job
name=${10};	#name for the job
descr=${11};	#description for the job

#basic param security filter
#re='^[0-9]+$';
#re='^[0-9]+([.][0-9]+)?$';
re='^[+-]?[0-9]+([.][0-9]+)?$';

#binary check
if [ "$binary" != "mtr" ] && [ "$binary" != "hping3" ] && [ "$binary" != "traceroute" ] ; then
	exit 1;
fi

if [ "$interval" != "5" ] && [ "$interval" != "10" ] && [ "$interval" != "15" ] && [ "$interval" != "30" ] && [ "$interval" != "60" ]; then
	exit 3;
fi

#end_stamp check
if ! [[ $end_stamp =~ $re ]] ; then
	exit 2;
else
	ts_diff=`echo "$end_stamp - $exec_date" | bc`;
	ts_threshold=`echo "$interval * 60 * 2" | bc`;
	if [ "$ts_diff" -le "$ts_threshold" ] ; then
        	exit 2;
	fi
fi

#proto check
if [ "$proto" != "tcp" ] && [ "$proto" != "udp" ] && [ "$proto" != "icmp" ] ; then
        exit 4;
fi

#src_port check
if ! [[ $src_port =~ $re ]] ; then
        exit 5;
else
	if [ "$src_port" -gt "65535" ] || [ "$src_port" -lt "1" ] ; then
        	exit 5;
	fi
fi

#dst_port check
if ! [[ $dst_port =~ $re ]] ; then
        exit 6;
else
	if [ "$dst_port" -gt "65535" ] || [ "$dst_port" -lt "1" ] ; then
        	exit 6;
	fi
fi

#psize check
if ! [[ $psize =~ $re ]] ; then
        exit 7;
else
	if [ "$psize" -gt "2000" ] || [ "$psize" -lt "0" ] ; then
        	exit 7;
	fi
fi

#count check;
if ! [[ $count =~ $re ]] ; then
        exit 8;
else
	if [ "$count" -gt "200" ] || [ "$count" -lt "1" ]; then
        	exit 8;
	fi
fi

# any regex for domain/ip/name/description
#if [] ; then
#        exit 9;
#fi

#creating actual job_id
job_id="`cat /dev/urandom | tr -dc "a-zA-Z0-9" | fold -w 32 | head -n 1`";
job_dir="$jobs/$job_id";
job_conf="$job_dir/.traceconf.sh";

#job dir creation
if [ "$prod" == "1" ] ; then
	mkdir $job_dir;
else
	echo -e "${BLUE}creating following directory:${NC}";
	echo -e "$job_dir \n";
fi

#prepare crontab entry
base="$tb/launch_trace.sh $job_id >/dev/null 2>&1";
if [ "$interval" == "5" ] || [ "$interval" == "10" ] || [ "$interval" == "15" ] || [ "$interval" == "30" ] ; then
	crontab_entry="*/$interval  * * * * $base";
elif [ "$interval" == "60" ] ; then
	crontab_entry="0 * * * * $base";
else
	crontab_entry="*/15  * * * * $base";
	interval="15";
fi

if [ "$prod" == "0" ] ; then
	echo -e "${BLUE}created crontab line:${NC}";
	echo -e  "$crontab_entry \n";
fi

#add crontab entry

if [ "$prod" == "1" ] ; then
	(crontab -l ; echo "$crontab_entry") | crontab;
else
	 echo -e "${BLUE}and updated actual crontab\n${NC}";
fi

#create trace config file
if [ "$prod" == "1" ] ; then
        typeset -p binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr > $job_conf
else
	echo -e "${BLUE}serializing params like below${NC}";
	typeset -p binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr
	echo -e "${BLUE}\nand storing in:${NC}";
	echo -e "$job_conf\n";
fi
