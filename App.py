import dash
from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    title="Glider Mission File",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

server = app.server

# Simple Navbar
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

# Main layout: navbar + page container
app.layout = dbc.Container(
    [navbar, dash.page_container],
    fluid=True
)

if __name__ == "__main__":
    app.run(debug=True)
