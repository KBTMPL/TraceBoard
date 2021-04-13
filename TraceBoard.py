import os
import cherrypy
import trace_jobs


class TraceBoard(object):
    @cherrypy.expose
    def index(self, job_id=None, reload=False):
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

            <!-- Optional theme -->
            <!-- <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"> -->

            <!-- Latest compiled and minified JavaScript -->
            <!-- <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script> -->
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
                                <a class="nav-link active" aria-current="page" href="#">Home</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="/?job_id=aaa">Schedule trace</a>
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
            
            <div id="container" class="mt-3" style="width:100%; height:400px;"></div>
            
            </div>
            
            <script>
            """ + trace_jobs.show_chart(job_id) + """
            
            function select_change() {
                var selected_job = document.getElementById("select_job");
                var selected_job_id = selected_job.value;
                var job_path = '/?job_id=' + selected_job_id;
                
                window.location = job_path;              
            }
            
            """ + "" + """
            </script>
        </body>
        </html>
        """


if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 8080
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './dirs'
        }
    }
    cherrypy.quickstart(TraceBoard(), '/', conf)
