import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from openai import OpenAI
from dotenv import load_dotenv
import os

# --- Load env vars and initialize OpenAI ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Register this page
dash.register_page(__name__, path="/", name="Home")

# --- Cards ---
search_card = dbc.Card(dbc.CardBody([html.H5("Search Bar", className="mb-3")]))
file_card   = dbc.Card(dbc.CardBody([html.H6("Drop Files", className="mb-3")]))
ma_card     = dbc.Card(dbc.CardBody([html.H6("Ma Files", className="mb-3")]))
mi_card     = dbc.Card(dbc.CardBody([html.H6("Mi Files", className="mb-3")]))

# --- Chat card with GPT integration ---
chat_card = dbc.Card(
    dbc.CardBody([
        html.H5("Chat with GPT", className="mb-3"),
        dcc.Store(id="chat-store", data=[]),
        dcc.Textarea(
            id="chat-input",
            placeholder="Type your message...",
            style={"width": "100%", "height": 100}
        ),
        html.Br(),
        dbc.Button("Send", id="chat-submit", color="primary", className="mt-2"),
        html.Div(
            id="chat-output",
            style={
                "marginTop": 20,
                "whiteSpace": "pre-line",
                "border": "1px solid #ccc",
                "padding": "10px",
                "borderRadius": "5px",
                "maxHeight": "300px",
                "overflowY": "auto"
            }
        ),
    ])
)

# --- Layout for this page ---
layout = dbc.Container(
    [
        html.H3("Glider Website"),
        dbc.Row([dbc.Col(search_card)]),
        dbc.Row([
            dbc.Col(file_card, width=6),
            dbc.Col(ma_card, width=3),
            dbc.Col(mi_card, width=3),
        ]),
        dbc.Row([dbc.Col(chat_card, width=12)], className="mt-4"),
    ],
    fluid=True
)

# --- Callbacks ---
@callback(
    Output("chat-store", "data"),
    Input("chat-submit", "n_clicks"),
    State("chat-input", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True
)
def update_chat_store(n_clicks, user_input, history):
    """Append user message, query GPT, and append assistant reply."""
    if not user_input:
        return history

    history.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant for mission file conversion."}] + history
        )
        assistant_msg = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_msg})
    except Exception as e:
        history.append({"role": "assistant", "content": f"Error: {str(e)}"})

    return history


@callback(
    Output("chat-output", "children"),
    Input("chat-store", "data")
)
def render_chat(history):
    if not history:
        return "Start the conversation above."

    rendered = []
    for msg in history:
        if msg["role"] == "user":
            rendered.append(html.Div([html.B("You: "), msg["content"]]))
        elif msg["role"] == "assistant":
            rendered.append(html.Div([html.B("Assistant: "), msg["content"]]))
        rendered.append(html.Hr(style={"margin": "4px 0"}))

    return rendered
