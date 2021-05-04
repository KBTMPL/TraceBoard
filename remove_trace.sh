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

# delete all data which belongs to trace
(crontab -l | sed "/$job_id/d") | crontab;
rm -rf $jobs/$job_id;
