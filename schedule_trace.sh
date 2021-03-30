#!/bin/bash

#init
tb="/home/kbulanda/kn2021/traceboard";
jobs="$tb/jobs";
prod="1";
exec_date=`date +%s`;
err_flag="0";

#miscellany
BLUE='\033[0;34m';
GREEN='\033[0;32m';
RED='\033[0;31m';
NC='\033[0m';

#test mode info
if [ "$prod" == "0" ] ; then
        echo -e "${GREEN}running in test mode no actions are actually done\n${NC}";
	if [[ $# -eq 0 ]] ; then
		echo -e "${RED}I see you did not provide any args and running in test mode grab this sample command:\n${NC}";
		echo -e './schedule_trace.sh mtr ` echo $(date "+%s") + 7201|bc` 15 icmp 1337 2137 1460 100 onet.pl\n'
	fi
fi

#new params intake
for i in "$@"
do
case $i in
    -e=*|--binary=*)
    binary="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--end_stamp=*)
    end_stamp="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--interval=*)
    interval="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--proto=*)
    proto="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--src_port=*)
    src_port="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--dst_port=*)
    dst_port="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--psize=*)
    psize="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--count=*)
    count="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--target=*)
    target="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--name=*)
    name="${i#*=}"
    shift # past argument=value
    ;;
    -e=*|--descr=*)
    descr="${i#*=}"
    shift # past argument=value
    ;;
    *)
          # unknown option
    ;;
esac
done

#basic param security filter
#re='^[0-9]+$';
#re='^[0-9]+([.][0-9]+)?$';
re='^[+-]?[0-9]+([.][0-9]+)?$';

#param count check

#binary check
if [ "$binary" != "mtr" ] && [ "$binary" != "hping3" ] && [ "$binary" != "traceroute" ] ; then
	err_flag=`echo $err_flag + 2 | bc`;
fi

if [ "$interval" != "5" ] && [ "$interval" != "10" ] && [ "$interval" != "15" ] && [ "$interval" != "30" ] && [ "$interval" != "60" ]; then
	err_flag=`echo $err_flag + 8 | bc`;
fi

#end_stamp check
if ! [[ $end_stamp =~ $re ]] ; then
	err_flag=`echo $err_flag + 4 | bc`;
else
	ts_diff=`echo "$end_stamp - $exec_date" | bc`;
	ts_threshold=`echo "$interval * 60 * 2" | bc`;
	if [ "$ts_diff" -le "$ts_threshold" ] ; then
        	err_flag=`echo $err_flag + 4 | bc`;
	fi
fi

#proto check
if [ "$proto" != "tcp" ] && [ "$proto" != "udp" ] && [ "$proto" != "icmp" ] ; then
        err_flag=`echo $err_flag + 16 | bc`;
fi

#src_port check
if ! [ -z "$src_port" ] ; then
	if ! [[ $src_port =~ $re ]] ; then
        	err_flag=`echo $err_flag + 32 | bc`;
	else
		if [ "$src_port" -gt "65535" ] || [ "$src_port" -lt "1" ] ; then
        		err_flag=`echo $err_flag + 32 | bc`;
		fi
	fi
fi

#dst_port check
if ! [ -z "$dst_port" ] ; then
	if ! [[ $dst_port =~ $re ]] ; then
        	err_flag=`echo $err_flag + 64 | bc`;
	else
		if [ "$dst_port" -gt "65535" ] || [ "$dst_port" -lt "1" ] ; then
        		err_flag=`echo $err_flag + 64 | bc`;
		fi
	fi
fi

#psize check
if ! [[ $psize =~ $re ]] ; then
        err_flag=`echo $err_flag + 128 | bc`;
else
	if [ "$psize" -gt "2000" ] || [ "$psize" -lt "0" ] ; then
        	err_flag=`echo $err_flag + 128 | bc`;
	fi
fi

#count check;
if ! [[ $count =~ $re ]] ; then
        err_flag=`echo $err_flag + 256 | bc`;
else
	if [ "$count" -gt "200" ] || [ "$count" -lt "1" ]; then
        	err_flag=`echo $err_flag + 256 | bc`;
	fi
fi

# any regex for domain/ip/name/description
#if [] ; then
#        exit 9;
#fi

if [ "$err_flag" -ne "0" ] ; then
	echo "$err_flag";
	exit 100;
fi

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
        typeset -p binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr > $job_conf  2>&1;
else
	echo -e "${BLUE}serializing params like below${NC}";
	typeset -p binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr
	echo -e "${BLUE}\nand storing in:${NC}";
	echo -e "$job_conf\n";
fi

echo "$err_flag";
exit "0";
