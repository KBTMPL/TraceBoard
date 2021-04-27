import os
import csv
from datetime import datetime
import re

jobs_path = "./jobs"


def get_job_name(job_id):
    job_name = ""
    if job_id is not None and job_id in os.listdir(jobs_path):
        job_conf_path = os.path.join(jobs_path, job_id, ".traceconf.sh")
        if os.path.exists(job_conf_path):
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
        if os.path.exists(job_conf_path):
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
    if ".healthcheck" in jobs:
        jobs.remove(".healthcheck")
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
        try:
            endstamp_date = datetime.fromtimestamp(int(job_details["end_stamp"])).strftime("%m/%d/%Y %H:%M:%S")
        except ValueError:
            endstamp_date = job_details["end_stamp"]
        printable_job_details = """
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
                            <th scope="row">End date</th>
                            <td>""" + endstamp_date + """</td>
                        </tr>
                        <tr>
                            <th scope="row">Interval [min]</th>
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
                            <th scope="row">Packet size [B]</th>
                            <td>""" + job_details["psize"] + """</td>
                        </tr>
                        <tr>
                            <th scope="row">Number of packets</th>
                            <td>""" + job_details["count"] + """</td>
                        </tr>
                    </tbody>
                </table>
        """

    return printable_job_details


def show_chart(selected_job_id):
    timestamp_list = list()
    loss_list = list()
    latency_list = list()
    if selected_job_id is not None and selected_job_id in os.listdir(jobs_path):
        selected_job_summary_path = os.path.join(jobs_path, selected_job_id, "tracesummary.csv")
        if os.path.exists(selected_job_summary_path):
            with open(selected_job_summary_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                rows = list(csv_reader)
                if len(rows) > 0:
                    if len(rows) > 15:
                        rows = rows[-15:]
                    for row in rows:
                        date_time = datetime.fromtimestamp(int(row[0]))
                        timestamp_list.append(date_time.strftime("%d/%m/%Y %H:%M:%S"))
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
                                plotOptions: {
                                    series: {
                                        cursor: 'pointer',
                                        point: {
                                            events: {
                                                click: function () {
                                                    show_trace_details(this.category);
                                                }
                                            }
                                        }
                                    }
                                },
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
            printable_show_chart = """ document.getElementById('chart_container').innerHTML='<div class="d-flex justify-content-center">No data available yet.</div>'"""
    else:
        printable_show_chart = """document.getElementById('container').style.display = 'none';"""
    return printable_show_chart


def get_health_check_status():
    health_job_path = os.path.join(jobs_path, ".healthcheck")
    if os.path.exists(health_job_path):
        health_summary_path = os.path.join(health_job_path, "tracesummary.csv")
        if os.path.exists(health_summary_path):
            with open(health_summary_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                rows = list(csv_reader)
                if len(rows) > 0:
                    last_trace = rows[-1]
                    try:
                        date_time = datetime.fromtimestamp(int(last_trace[0]))
                        timestamp_date = date_time.strftime("%d/%m/%Y %H:%M:%S")
                        loss = str(last_trace[1]).replace("%", "")
                        latency = str(last_trace[2])

                        health_last_trace_path = os.path.join(health_job_path, str(last_trace[0]))
                        if os.path.exists(health_last_trace_path):
                            with open(health_last_trace_path) as trace_file:
                                content = trace_file.read()
                        else:
                            content = "No trace file available."

                        printable_last_trace_info = """
                                <div id="container" class="container-fluid mb-4">
                                    <div class="row">
                                        <div class="col-4 my-3">
                                            <div class="alert alert-primary container-fluid" role="alert">
                                                <h5>Timestamp date</h5>
                                                <p>""" + timestamp_date + """</p>
                                            </div>
                                        </div>
                                        <div class="col-4 my-3">
                                            <div class="alert alert-primary container-fluid" role="alert">
                                                <h5>Loss</h5>
                                                <p>""" + loss + """%</p>
                                            </div>
                                        </div>
                                        <div class="col-4 my-3">
                                            <div class="alert alert-primary container-fluid" role="alert">
                                                <h5>Average latency</h5>
                                                <p>""" + latency + """ ms</p>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div id="last_health_check_trace" class="overflow-scroll container-fluid" style="white-space:pre-line; height:300px">
                                                """ + content + """
                                            </div>
                                        </div>
                                    </div>
                        """
                    except ValueError:
                        printable_last_trace_info = """<p>No data available.</p>"""
                else:
                    printable_last_trace_info = """<p>No data available yet</p>"""
        else:
            printable_last_trace_info = """<p>No data available yet</p>"""
        printable_health_check = """
                 <div id="container" class="container-fluid mb-4">
                 <div class="row">
                    <div class="col-xxl-4 my-3">""" + show_job_details_info(".healthcheck") + """</div>
                    <div class="col-xxl-8 my-3">
                        <div class="container-fluid mb-3">
                            <h3 class="mb-3">Last trace status</h3>
                            """ + printable_last_trace_info + """
                        </div>
                    </div>
                 </div>
                 </div>
                 """
    else:
        printable_health_check = """
                <div class="alert alert-secondary mt-3" role="alert">
                    No health check configured.
                </div>
                """
    return printable_health_check
