import atexit
import logging
import os
import json
import subprocess
from pathlib import Path

from bokeh.embed import server_document
from flask import Flask, request
from flask import render_template

project_dir = Path(__file__).resolve().parents[1]
print(project_dir)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

app = Flask(__name__)
app.config["SECRET_KEY"] = "hello_lifeplayer"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
#
path_to_bokeh_py = f"{project_dir}/lifeplayer_app/lifeplayer_plot.py"
if os.getenv('bokeh_runs', 'no') == 'no':
    bokeh_process = subprocess.Popen(
        [
            "python",
            "-m",
            "panel",
            "serve",
            "--allow-websocket-origin=localhost:5000",
            path_to_bokeh_py,
        ],
        stdout=subprocess.PIPE,
    )
    os.environ['bokeh_runs'] = 'yes'


@atexit.register
def kill_server():
    bokeh_process.kill()
    os.environ['bokeh_runs'] = 'no'


@app.route("/lifeplayer_plot", methods=['GET', 'POST'])
def life_player_json():
    data = request.get_json()
    print(f'Flask side: {data}')
    script = server_document(
        url="http://localhost:5006/lifeplayer_plot", arguments=data)
    print(script)
    return render_template("lifeplayer_template.html", bokeh_script=script)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
