#!/bin/bash

#TO DO!
#

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
        echo -e "${GREEN}running in test mode additional output will be provided\n${NC}";
fi

if ! [[ $# -eq 1 ]] ; then
	if [ "$prod" == "0" ] ; then
		echo -e "${RED}No job id was given will not proceed further\n${NC}";
	fi
	exit "100";
else
	job_id="$1";
	job_conf="$jobs/$job_id/.traceconf.sh";
	if [ -f "$job_conf" ] ; then
		source "$job_conf";
		for var in binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr;
		do
			if [ "${!var}" == "N/A" ] ; then
				unset `echo "$var"`;
			fi
		done
	else
		if [ "$prod" == "0" ] ; then
                	echo -e "${RED}$job_conf does not exist\n${NC}";
        	fi
		exit "100";
	fi
fi

if [ "$job_id" == ".healthcheck" ] ; then
	healthcheck="1";
else
	healthcheck="0";
fi

#vars: binary end_stamp interval proto src_port dst_port psize count target tb jobs job_id job_dir job_conf name descr

#remove job if it is outdated and stop from proceeding further - only if it is not healthcheck
if [ "$healthcheck" == "0" ] ; then
	if [ "$exec_date" -gt "$end_stamp" ] ; then
		(crontab -l | sed "/$job_id/d") | crontab;
		exit "100":
	fi
fi

#mtr section
if [ "$binary" == "mtr" ] ; then
	if [ "$proto" == "tcp" ] ; then
		cmd="mtr --report-wide -rbzc $count --psize $psize --tcp `if ! [[ -z $src_port ]]; then echo \"-L $src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"-P $dst_port\"; fi` $target";
	fi
	if [ "$proto" == "udp" ] ; then
		cmd="mtr --report-wide -rbzc $count --psize $psize --udp `if ! [[ -z $src_port ]]; then echo \"-L $src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"-P $dst_port\"; fi` $target";
	fi
	if [ "$proto" == "icmp" ] ; then
		cmd="mtr --report-wide -rbzc $count --psize $psize $target";
	fi
fi

#traceroute section
if [ "$binary" == "traceroute" ] ; then
        if [ "$proto" == "tcp" ] ; then
		cmd="traceroute -T -q $count `if ! [[ -z $src_port ]]; then echo \"--sport=$src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"--port=$dst_port\"; fi` $target $psize";
        fi
        if [ "$proto" == "udp" ] ; then
		cmd="traceroute -q $count `if ! [[ -z $src_port ]]; then echo \"--sport=$src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"--port=$dst_port\"; fi` $target $psize";
        fi
        if [ "$proto" == "icmp" ] ; then
		cmd="traceroute -I -q $count $target $psize";
        fi
fi

#hping3 section
if [ "$binary" == "hping3" ] ; then
        if [ "$proto" == "tcp" ] ; then
                cmd="hping3 -S -c $count `if ! [[ -z $src_port ]]; then echo \"--baseport $src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"--destport $dst_port\"; fi` -d $psize $target";
        fi
        if [ "$proto" == "udp" ] ; then
                cmd="hping3 -S --udp -c $count `if ! [[ -z $src_port ]]; then echo \"--baseport $src_port\"; fi` `if ! [[ -z $dst_port ]]; then echo \"--destport $dst_port\"; fi` -d $psize $target";
        fi
        if [ "$proto" == "icmp" ] ; then
                cmd="hping3 --icmp -c $count -d $psize $target";
        fi
fi

#execute command
sudo `echo $cmd` > $job_dir/$exec_date 2>&1 && pango-view --font=mono -qo $job_dir/$exec_date.svg $job_dir/$exec_date

if [ "$binary" == "mtr" ] ; then
	#Loss%   Snt   Avg  Best  Wrst StDev  Last
	prepped_line=`tail -n1 $job_dir/$exec_date | awk '{print $5";"$6";"$8";"$9";"$10";"$11";"$7}'`
	echo "$exec_date;$prepped_line" >> $job_dir/tracesummary.csv;
fi
if [ "$binary" == "traceroute" ] ; then
	#Loss%   Snt   Avg  Best  Wrst StDev
	unreachable_count=`tail -n1 $job_dir/$exec_date | sed 's/ms//g' | awk '{for(i=4;i<=NF;i++){printf "%s ", $i}; printf "\n"}' | tr ' ' '\n' |grep -c '*'`;
	total_count=`tail -n1 $job_dir/$exec_date | sed 's/ms//g' | awk '{for(i=4;i<=NF;i++){printf "%s ", $i}; printf "\n"}' | wc -w`;
	packet_loss=`echo "scale=2;$unreachable_count/$total_count*100" | bc`;
	if ! [ "$unreachable_count" -eq "$total_count" ] ; then
		maths=`tail -n1 $job_dir/$exec_date | sed 's/ms//g' | awk '{for(i=4;i<=NF;i++){printf "%s ", $i}; printf "\n"}' | xargs | tr ' ' '\n' | jq -s '{best:min,wrst:max,average:(add/length),stddev:((add/length)as $a|map(pow(.-$a;2))|add/(length-1)|sqrt) } | map(.) | @csv' | sed  "s/\"//g" | sed "s/,/;/g"`;
	else
		maths='0;0;0;0'
	fi
	echo "$exec_date;$packet_loss%;$total_count;$maths" >> $job_dir/tracesummary.csv;
fi
if [ "$binary" == "hping3" ] ; then
	#Loss%   Snt   Avg  Best  Wrst
	prepped_line=`grep -E 'packet|round' $job_dir/$exec_date | xargs | sed 's/\// /g' | awk '{print $7";"$1";"$16";"$15";"$17}'`
	echo "$exec_date;$prepped_line" >> $job_dir/tracesummary.csv;
fi
