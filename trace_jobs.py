import os
import csv
from datetime import datetime

jobs_path = ""


def list_jobs_dropdown(selected_job_id):
    jobs = os.listdir(jobs_path)
    dropdown_job_list = list()
    for job in jobs:
        if job == str(selected_job_id):
            dropdown_job_list.append('<option selected value="' + job + '">' + job + '</option>')
        else:
            dropdown_job_list.append('<option value="' + job + '">' + job + '</option>')
    printable_dropdown_job_list = "\n".join(dropdown_job_list)
    return printable_dropdown_job_list


def show_chart(selected_job_id):
    timestamp_list = list()
    loss_list = list()
    latency_list = list()
    if selected_job_id is not None and selected_job_id in os.listdir(jobs_path):
        selected_job_path = os.path.join(jobs_path, selected_job_id, "tracesummary.csv")
        with open(selected_job_path) as csv_file:
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
                        const chart = Highcharts.chart('container', {
                            chart: {
                                type: 'line'
                            },
                            chart: {
                                zoomType: 'xy'
                            },
                            title: {
                                text: 'Job ID: """ + selected_job_id + """'
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
