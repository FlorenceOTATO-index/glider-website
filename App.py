import dash
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc
from flask import request, jsonify
import os, subprocess

# Import your RAG pipeline
from rag import answer

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Glider Mission File",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server  # Flask instance inside Dash

# -------------------------------
# Flask routes for RAG
# -------------------------------

UPLOAD_FOLDER = "kb"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@server.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Re-run ingestion so KB is updated
    subprocess.run(["python3", "ingest.py"], check=True)

    return jsonify({"message": f"{file.filename} uploaded and ingested"})


@server.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = answer(query)
    return jsonify({"answer": response})


# -------------------------------
# Dash layout
# -------------------------------

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Map", href="/map", active="exact")
    ],
    brand="File Conversion",
    brand_style={"fontSize": "25px"},
    style={"backgroundColor": "#6B90A5"},
    className="mb-2"
)

# Only navbar + page container (no extra upload/ask UI here)
app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True
)

if __name__ == "__main__":
    app.run(debug=True)
