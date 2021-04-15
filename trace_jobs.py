import os
import csv
from datetime import datetime
import re

jobs_path = ""


def get_job_name(job_id):
    job_name = ""
    if job_id is not None and job_id in os.listdir(jobs_path):
        job_conf_path = os.path.join(jobs_path, job_id, ".traceconf.sh")
        with open(job_conf_path) as conf_file:
            content = list(conf_file)
            if "name: not found" not in content[14]:
                job_name = re.sub(r'^.*?"', '"', content[14]).replace('"', '').strip()
    return job_name


def get_job_conf_info(job_id):
    job_info_dict = {
        "id": job_id,
        "name": get_job_name(job_id),
        "descr": "",
        "binary": "",
        "end_stamp": "",
        "interval": "",
        "proto": "",
        "src_port": "",
        "dst_port": "",
        "psize": "",
        "count": "",
        "target": ""
    }
    dict_list_position = {
        "descr": 15,
        "binary": 0,
        "end_stamp": 1,
        "interval": 2,
        "proto": 3,
        "src_port": 4,
        "dst_port": 5,
        "psize": 6,
        "count": 7,
        "target": 8
    }
    if job_id is not None and job_id in os.listdir(jobs_path):
        job_conf_path = os.path.join(jobs_path, job_id, ".traceconf.sh")
        with open(job_conf_path) as conf_file:
            content = list(conf_file)
            for info_type in dict_list_position.keys():
                if "not found" in content[dict_list_position[info_type]]:
                    job_info_dict[info_type] = "N/A"
                else:
                    job_info_dict[info_type] = re.sub(r'^.*?"', '"', content[dict_list_position[info_type]]).replace('"', '').strip()
    return job_info_dict


def list_jobs_dropdown(selected_job_id):
    jobs = os.listdir(jobs_path)
    dropdown_job_list = list()
    for job in jobs:
        job_select_option = job
        job_name = get_job_name(job)
        if job_name:
            job_select_option = job_select_option + ": " + job_name
        if job == str(selected_job_id):
            dropdown_job_list.append('<option selected value="' + job + '">' + job_select_option + '</option>')
        else:
            dropdown_job_list.append('<option value="' + job + '">' + job_select_option + '</option>')
    printable_dropdown_job_list = "\n".join(dropdown_job_list)
    return printable_dropdown_job_list


def show_job_details_info(selected_job_id):
    printable_job_details = ""
    if selected_job_id is not None and selected_job_id in os.listdir(jobs_path):
        job_details = get_job_conf_info(selected_job_id)
        printable_job_details = """
                <div class="chart_container">
                    <table class="table">
                        <tbody>
                            <tr>
                                <th scope="row">Job ID</th>
                                <td>""" + job_details["id"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Job Name</th>
                                <td>""" + job_details["name"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Description</th>
                                <td>""" + job_details["descr"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Binary</th>
                                <td>""" + job_details["binary"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Target</th>
                                <td>""" + job_details["target"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">End timestamp</th>
                                <td>""" + job_details["end_stamp"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Interval</th>
                                <td>""" + job_details["interval"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Protocol</th>
                                <td>""" + job_details["proto"].upper() + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Source port</th>
                                <td>""" + job_details["src_port"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Destination port</th>
                                <td>""" + job_details["dst_port"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Packet size</th>
                                <td>""" + job_details["psize"] + """</td>
                            </tr>
                            <tr>
                                <th scope="row">Number of packets</th>
                                <td>""" + job_details["count"] + """</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
        """

    return printable_job_details


def show_chart(selected_job_id):
    timestamp_list = list()
    loss_list = list()
    latency_list = list()
    if selected_job_id is not None and selected_job_id in os.listdir(jobs_path):
        print(get_job_conf_info(selected_job_id))
        selected_job_summary_path = os.path.join(jobs_path, selected_job_id, "tracesummary.csv")
        with open(selected_job_summary_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            rows = list(csv_reader)
            if len(rows) > 0:
                for row in rows:
                    date_time = datetime.fromtimestamp(int(row[0]))
                    timestamp_list.append(date_time.strftime("%m/%d/%Y %H:%M:%S"))
                    loss_list.append(str(row[1]).replace("%", ""))
                    latency_list.append(str(row[2]))

        printable_show_chart = """
                    document.addEventListener('DOMContentLoaded', function () {
                        const chart = Highcharts.chart('chart_container', {
                            chart: {
                                type: 'line'
                            },
                            chart: {
                                zoomType: 'xy'
                            },
                            title: {
                                text: 'Loss & Average Latency Plot'
                            },
                            xAxis: {
                                categories: ['""" + "','".join(timestamp_list) + """']
                            },
                            yAxis: [{  
                                labels: {
                                    format: '{value}%'
                                },
                                title: {
                                    text: 'Loss [%]'
                                }
                            }, {
                                labels: {
                                    format: '{value} ms'
                                },
                                title: {
                                    text: 'Latency [ms]'
                                },
                                opposite: true
                            }],
                            series: [{
                                name: 'Loss',
                                data: [""" + ",".join(loss_list) + """]
                            }, {
                                name: 'Average Latency',
                                yAxis: 1,
                                data: [""" + ",".join(latency_list) + """]
                            }]
                        });
                    });
                    """
    else:
        printable_show_chart = """document.getElementById('container').style.display = 'none';"""
    return printable_show_chart
