import os
import shutil
from pyramid.response import Response

from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound, HTTPForbidden

from check_benford import check_benford


@view_config(
        route_name="home", 
        renderer="templates/home.jinja2"
)
def home_view(request):
    if request.method == "POST":
        filename = request.POST['CSVfile'].filename

        if filename.split(".")[-1].lower() == "csv":
            input_file = request.POST["CSVfile"].file

            file_path = os.path.join('csvFiles', filename)

            with open(file_path, 'wb') as output_file:
                shutil.copyfileobj(input_file, output_file)

            return HTTPFound(location=request.route_url("output", filename=filename))
        
        else:
            return HTTPFound(location=request.route_url("error", error_type="file-upload-error"))
    
    return {}

    

@view_config(
        route_name="output",
        renderer="json"
)
def output_view(request):
    filename = request.matchdict['filename']

    if filename == "random":
        benford_proof, output = check_benford(file=None, random_dist=True)
    else:
        file = os.path.join('csvFiles', filename)
        benford_proof, output = check_benford(file)

    if benford_proof:
        return {
                "Accept": True,
                "output": output
        }
    else:
        return HTTPFound(location=request.route_url("error", error_type="reject-law"))


@view_config(
        route_name="error"
)
def file_upload_error_view(request):
    error_msg = request.matchdict["error_type"]
    if error_msg == "file-upload-error":
        raise HTTPForbidden("Upload file in CSV format")
    elif error_msg == "reject-law":
        return Response("<h3>The distribution doesnot accept Brenford Law.</h3>")





