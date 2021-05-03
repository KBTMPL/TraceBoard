import os
import cherrypy
import trace_jobs


class TraceBoard(object):
    @cherrypy.expose
    def index(self, reload=False):
        return """
        <!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <meta name="description" content="Trace Board">
            <meta name="author" content="Anna Bulanda & Krzysztof Bulanda">

            <title>Trace Board</title>

            <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>

            <!-- Latest compiled and minified CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

            <!-- Latest compiled and minified JavaScript -->
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>
            
            <!-- Highcharts -->
            <script src="https://code.highcharts.com/highcharts.src.js"></script>     
            <style>
                .trace {
                    width:100%;
                    height:auto;
                }
            </style>
        </head>
        <body>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                <div class="container-fluid">
                    <a class="navbar-brand" href="#">Trace Board</a>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item">
                                <a class="nav-link active" aria-current="page" href="/">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/trace_jobs">Trace jobs</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/schedule_trace">Schedule trace</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            <div class="mx-3">
                <h1 class="my-4">Welcome to Trace Board!</h1>
                <div class="my-4">
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
                    Ut imperdiet velit sed turpis hendrerit, ac bibendum ligula vehicula. 
                    Suspendisse eu leo fermentum eros maximus bibendum. 
                    Vestibulum pharetra odio sit amet diam tempus lacinia. 
                    Curabitur lorem nisi, ultrices vel auctor non, pellentesque vitae lectus.
                    Vestibulum ac blandit purus. 
                    Vivamus sagittis accumsan lacus, ac rutrum urna efficitur quis. 
                    Vivamus a purus condimentum erat blandit rhoncus nec eu sapien. 
                    Etiam ligula risus, sagittis vel est vel, posuere imperdiet diam. 
                    Nullam leo metus, aliquam non semper sit amet, hendrerit eget mauris. 
                    Sed a ante vitae quam consequat posuere. Phasellus at justo orci. 
                    Vestibulum ultricies varius placerat. Praesent hendrerit consectetur odio nec faucibus.</p>
                </div>
                <h2 class="mt-5">Health check status</h2>
                """ + trace_jobs.get_health_check_status() + """
            </div>
        </body>
        <script>
            """ + trace_jobs.get_health_check_last_trace_js() + """
        </script>
        </html>
        """

    @cherrypy.expose
    def trace_jobs(self, job_id=""):
        return """
               <!DOCTYPE html>
               <html lang="pl">
               <head>
                   <meta charset="utf-8">
                   <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                   <meta name="description" content="Trace Board">
                   <meta name="author" content="Anna Bulanda & Krzysztof Bulanda">

                   <title>Trace Board</title>

                   <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>

                   <!-- Latest compiled and minified CSS -->
                   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css">
                   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

                   <!-- Latest compiled and minified JavaScript -->
                   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
                   <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>

                   <!-- Highcharts -->
                   <script src="https://code.highcharts.com/highcharts.src.js"></script>     
                   <style>
                   .trace {
                       width:90%;
                       height:auto;
                   }
                   </style>
               </head>
               <body>
                   <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                       <div class="container-fluid">
                           <a class="navbar-brand" href="#">Trace Board</a>
                           <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                               <span class="navbar-toggler-icon"></span>
                           </button>
                           <div class="collapse navbar-collapse" id="navbarSupportedContent">
                               <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                   <li class="nav-item">
                                       <a class="nav-link" aria-current="page" href="/">Home</a>
                                   </li>
                                   <li class="nav-item">
                                        <a class="nav-link active" href="/trace_jobs">Trace jobs</a>
                                    </li>
                                   <li class="nav-item">
                                       <a class="nav-link" href="/schedule_trace">Schedule trace</a>
                                   </li>
                               </ul>
                           </div>
                       </div>
                   </nav>

                   <div class="mx-3">
                       <h1 class="my-4">Job list</h1>

                       <select class="form-select my-4" id="select_job" aria-label="Select job" onchange="select_change()">
                           <option selected value="" disabled selected hidden>Choose job from list</option>
                           """ + trace_jobs.list_jobs_dropdown(job_id) + """
                       </select>


                       <div id="container" class="container-fluid mb-4" style="background-color:#f0f2f4">
                           <div class="row">
                               <div class="col-xxl-4 my-3 d-flex justify-content-center">""" + trace_jobs.show_job_details_info(job_id) + """</div>
                               <div class="col-xxl-8 my-3 d-flex align-items-center"><div id="chart_container" style="width:100%; height:600px"></div></div>
                           </div>
                           <div class="row">
                               <div class="col-xxl-12 me-2 mb-3">
                                   <div class="card" id="show_trace" style="background-color:#fefefe">
                                       <p class="card-title mt-2 mx-3" id="trace_date"></p>
                                       <a id="trace_details_link"><img id="trace" class="trace"/></a>
                                   </div>
                               </div>
                           </div>
                       </div>
                   </div>


                   <script>
                   """ + trace_jobs.show_chart(job_id) + """

                   document.getElementById('show_trace').style.display = 'none';

                   function select_change() {
                       var selected_job = document.getElementById("select_job");
                       var selected_job_id = selected_job.value;
                       var job_path = '/trace_jobs?job_id=' + selected_job_id;

                       window.location = job_path;
                   }

                   function show_trace_details(trace_date) {
                       var selected_job = document.getElementById("select_job");
                       var selected_job_id = selected_job.value;
                       var trace_date_split = trace_date.split(" ");
                       var date = trace_date_split[0].split("/");
                       var time = trace_date_split[1].split(":");
                       var timestamp = new Date( date[2], date[1] - 1, date[0], time[0], time[1], time[2])/1000;
                       var trace_path = selected_job_id + "/" + timestamp.toString();

                       document.getElementById('trace_date').innerHTML='Trace from: ' + trace_date;
                       document.getElementById('show_trace').style.display = 'block';

                       $("#trace").attr("src", "/static/" + trace_path + ".svg")
                       $("#trace_details_link").attr("href", "/static/" + trace_path);
                       $("#trace_details_link").attr("download", "/static/" + trace_path + ".txt");

                       window.location.hash = "show_trace";
                   }

                   </script>
               </body>
               </html>
               """

    @cherrypy.expose
    def schedule_trace(self, reload=False):
        return """
            <!DOCTYPE html>
            <html lang="pl">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <meta name="description" content="Trace Board">
                <meta name="author" content="Anna Bulanda & Krzysztof Bulanda">

                <title>Trace Board</title>

                <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.js"></script>

                <!-- Latest compiled and minified CSS -->
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">

                <!-- Latest compiled and minified JavaScript -->
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.1/dist/umd/popper.min.js" integrity="sha384-SR1sx49pcuLnqZUnnPwx6FCym0wLsk5JZuNx2bPPENzswTNFaQU1RDvt3wT4gWFG" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.min.js" integrity="sha384-j0CNLUeiqtyaRmlzUHCPZ+Gy5fQu0dQ6eZ/xAww941Ai1SxSY+0EQqNXNE6DZiVc" crossorigin="anonymous"></script>

                <!-- Highcharts -->
                <script src="https://code.highcharts.com/highcharts.src.js"></script>
            </head>
            <body>
                <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
                    <div class="container-fluid">
                        <a class="navbar-brand" href="#">Trace Board</a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                <li class="nav-item">
                                    <a class="nav-link" aria-current="page" href="/">Home</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="/trace_jobs">Trace jobs</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link active" href="/schedule_trace">Schedule trace</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <div class="mx-3">
                    <h1 class="my-4">Schedule new trace</h1>
                    <form method="post" action="schedule_trace">
                        <div class="mb-3">
                            <label for="inputName" class="form-label">Name</label>
                            <input type="text" class="form-control" id="name" placeholder="Name">
                        </div>
                        <div class="mb-3">
                            <label for="inputDescription" class="form-label">Description</label>
                            <textarea class="form-control" id="descr" rows="3" placeholder="Description"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="inputTarget" class="form-label">Target</label>
                            <input type="text" class="form-control" id="target" placeholder="Target" required>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="inputBinary" class="form-label">Binary</label>
                                <select name="binary" class="form-select" id="binary" form="binaryform">
                                    <option selected value="" disabled selected hidden>Choose binary</option>
                                    <option value="mtr">mtr</option>
                                    <option value="traceroute">traceroute</option>
                                    <option value="hping3">hpin3</option>
                                </select>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="inputProtocol" class="form-label">Protocol</label>
                                <select name="proto" class="form-select" id="proto" form="protoform" onchange="proto_change()">
                                    <option selected value="" disabled selected hidden>Choose protocol</option>
                                    <option value="tcp">TCP</option>
                                    <option value="udp">UDP</option>
                                    <option value="icmp">ICMP</option>
                                </select>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="inputSrcPort" class="form-label">Source port</label>
                                <input type="number" class="form-control" id="src_port">
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="inputDstPort" class="form-label">Destination port</label>
                                <input type="number" class="form-control" id="dst_port">
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="inputDate" class="form-label">End date</label>
                                <input type="date" class="form-control" id="end_date" required>
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="inputTime" class="form-label">End time</label>
                                <input type="time" class="form-control" id="end_time" required>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-4 mb-3">
                                <label for="inputInterval" class="form-label">Interval</label>
                                <select name="interval" class="form-select" id="interval" form="intervalform">
                                    <option selected value="" disabled selected hidden>Choose interval</option>
                                    <option value="5">5 min</option>
                                    <option value="10">10 min</option>
                                    <option value="15">15 min</option>
                                    <option value="30">30 min</option>
                                    <option value="60">60 min</option>
                                </select>
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="inputCount" class="form-label">Count</label>
                                <input type="number" class="form-control" id="count">
                            </div>
                            <div class="col-md-4 mb-3">
                                <label for="inputPsize" class="form-label">Packet size</label>
                                <input type="number" class="form-control" id="psize">
                            </div>
                        </div>
                        <div class="mb-3 mt-2 form-check">
                            <input type="checkbox" class="form-check-input" id="healthcheck" onclick="healthcheck_change()">
                            <label class="form-check-label" for="healthCheck">Health check</label>
                        </div>
                        <div class="text-center my-4">
                            <button type="submit" class="btn btn-primary">Submit</button>
                        </div>
                    </form>
                </div>
            </body>
             <script>
                 function proto_change() {
                     var selected_proto = document.getElementById("proto").value;
                     if (selected_proto == "icmp") {
                          $("#src_port").attr("disabled", "true");
                          $("#dst_port").attr("disabled", "true");
                          $("#src_port").val("");
                          $("#dst_port").val("");
                     }
		     else {
                          $("#src_port").removeAttr("disabled");
                          $("#dst_port").removeAttr("disabled");
                     }
                 }
                 function healthcheck_change() {
                     if (document.getElementById("healthcheck").checked) {
                          $("#end_date").removeAttr("required");
                          $("#end_time").removeAttr("required");
                          $("#end_date").attr("disabled", "true");
                          $("#end_time").attr("disabled", "true");
                          $("#end_date").val("");
                          $("#end_time").val("");
                     }
                     else {
                          $("#end_date").removeAttr("disabled");
                          $("#end_time").removeAttr("disabled");
                          $("#end_date").attr("required", "true");
                          $("#end_time").attr("required", "true");
                     }
                 }
            </script>
            </html>
            """


if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './jobs'
        }
    }
    cherrypy.quickstart(TraceBoard(), '/', conf)
