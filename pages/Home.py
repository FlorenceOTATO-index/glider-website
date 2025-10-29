import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from dash import dcc, html, Input, Output, State, callback


# -----------------------------
# OpenAI setup
# -----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dash.register_page(__name__, path="/", name="Home")

# -----------------------------
# UI helpers
# -----------------------------
def chat_bubble(role, content):
    who = "You" if role == "user" else "Assistant"
    bubble_style = {
        "border": "1px solid #ddd",
        "borderRadius": "8px",
        "padding": "8px 10px",
        "margin": "6px 0",
        "backgroundColor": "#fff" if role == "user" else "#f4f8ff",
        "whiteSpace": "pre-wrap",
        "wordBreak": "break-word",
    }
    return html.Div([html.B(f"{who}: "), html.Span(content)], style=bubble_style)

def file_panel(title, store_id, color="light"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H6(title, className="mb-3"),
                html.Div(
                    id=f"{store_id}-view",
                    style={
                        "border": "1px solid #e5e5e5",
                        "borderRadius": "6px",
                        "padding": "8px",
                        "maxHeight": "280px",
                        "overflowY": "auto",
                        "backgroundColor": "#fafafa",
                        "fontFamily": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
                        "fontSize": "12.5px",
                    },
                ),
            ]
        ),
        color=color,
        className="h-100",
    )

def decode_text_from_upload(contents):
    """
    contents is a 'data:*/*;base64,<payload>' string from dcc.Upload.
    Returns decoded text (utf-8) or None if not text-like.
    """
    try:
        if contents is None:
            return None
        header, b64 = contents.split(",", 1)
        raw = base64.b64decode(b64)
        # We assume mission files are text. If this fails, we treat as binary and return None.
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return None

def short_preview(txt, limit=500):
    if txt is None:
        return "(binary/non-text content)"
    t = txt.strip()
    return t if len(t) <= limit else f"{t[:limit]}...\n[truncated]"

# -----------------------------
# Layout
# -----------------------------
chat_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Chat with GPT", className="mb-3"),

            # Stores
            dcc.Store(id="chat-store", data=[]),
            dcc.Store(id="mi-files-store", data=[]),   # list of dicts: {name, content}
            dcc.Store(id="ma-files-store", data=[]),   # list of dicts: {name, content}

            # Error area for upload validation
            dbc.Alert(id="upload-error", is_open=False, color="danger", duration=4000),

            # Unified Upload (entrance to Chat + file panels)
            dcc.Upload(
                id="file-upload",
                children=html.Div(["📂 Drag & Drop `.mi` / `.ma` here, or ", html.A("Browse")]),
                style={
                    "width": "100%",
                    "height": "70px",
                    "lineHeight": "70px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "6px",
                    "textAlign": "center",
                    "marginBottom": "12px",
                    "backgroundColor": "#fbfbfb",
                },
                multiple=True,
                accept=".mi,.ma",  # front-end accept
            ),

            # Row with MA / MI panels
            # --- Ma/Mi resizable row (fixed height, draggable middle bar) ---
            # --- Ma/Mi resizable row (fixed height, draggable middle bar) ---
            html.Div(
                [
                    html.Div(
                        file_panel("Ma Files (.ma)", "ma-files-store"),
                        id="ma-panel",
                        style={
                            "flex": "1",
                            "minWidth": "200px",
                            "height": "520px",        # fixed tall height
                            "overflowY": "auto",
                        },
                    ),
                    html.Div(
                        id="dragbar",
                        style={
                            "width": "8px",
                            "cursor": "col-resize",
                            "backgroundColor": "#c9ced6",
                            "margin": "0 6px",
                            "borderRadius": "4px",
                            "userSelect": "none",  
                            "pointerEvents": "auto",
                        },
                    ),
                    html.Div(
                        file_panel("Mi Files (.mi)", "mi-files-store"),
                        id="mi-panel",
                        style={
                            "flex": "1",
                            "minWidth": "200px",
                            "height": "520px",        # fixed tall height
                            "overflowY": "auto",
                        },
                    ),
                ],
                id="split-container",
                style={
                    "display": "flex",
                    "alignItems": "stretch",
                    "border": "1px solid #e1e5ea",
                    "borderRadius": "8px",
                    "padding": "6px",
                    "marginBottom": "14px",
                    "height": "520px",              # parent locks the total height
                    "backgroundColor": "#f7f9fc",
                },
            ),


            # Text entry
            dcc.Textarea(
                id="chat-input",
                placeholder="Type your message… (files dropped above will appear here as attachments)",
                style={"width": "100%", "height": 100},
            ),
            dbc.Button("Send", id="chat-submit", color="primary", className="mt-2"),

            # Chat view
            html.Div(
                id="chat-output",
                style={
                    "marginTop": 16,
                    "border": "1px solid #e5e5e5",
                    "padding": "10px",
                    "borderRadius": "6px",
                    "maxHeight": "420px",
                    "overflowY": "auto",
                    "backgroundColor": "#f9f9f9",
                },
            ),
        ]
    )
)

layout = dbc.Container(
    [
        html.H3("Glider Website", className="mb-3"),
        chat_card,
    ],
    fluid=True,
)

# -----------------------------
# Callbacks
# -----------------------------

@callback(
    Output("chat-store", "data"),
    Output("mi-files-store", "data"),
    Output("ma-files-store", "data"),
    Output("upload-error", "children"),
    Output("upload-error", "is_open"),
    Input("file-upload", "contents"),
    State("file-upload", "filename"),
    State("chat-store", "data"),
    State("mi-files-store", "data"),
    State("ma-files-store", "data"),
    prevent_initial_call=True,
)
def handle_upload(contents_list, filenames, chat_hist, mi_files, ma_files):
    """
    Accept only .mi / .ma. On valid upload:
      - Append a 'user' message into chat with a short preview.
      - Store full file text into the appropriate store (mi vs ma).
    Show a banner if any invalid files were dropped.
    """
    chat_hist = chat_hist or []
    mi_files = mi_files or []
    ma_files = ma_files or []

    if not contents_list or not filenames:
        return chat_hist, mi_files, ma_files, "", False

    invalid = []
    new_msgs = []

    for contents, fname in zip(contents_list, filenames):
        fname_lower = (fname or "").lower().strip()

        if fname_lower.endswith(".mi") or fname_lower.endswith(".ma"):
            text = decode_text_from_upload(contents)
            pv = short_preview(text, limit=600)

            # append to chat as "copied into chat"
            ext = ".mi" if fname_lower.endswith(".mi") else ".ma"
            new_msgs.append(
                {"role": "user", "content": f"📎 Uploaded file {ext}: {fname}\n\nPreview:\n{pv}"}
            )

            # store to respective box
            rec = {"name": fname, "content": text or ""}
            if ext == ".mi":
                mi_files.append(rec)
            else:
                ma_files.append(rec)
        else:
            invalid.append(fname or "(unnamed)")

    chat_hist.extend(new_msgs)

    if invalid:
        msg = (
            "Rejected non-mission files: "
            + ", ".join(invalid)
            + ". Only .mi and .ma are accepted."
        )
        return chat_hist, mi_files, ma_files, msg, True

    return chat_hist, mi_files, ma_files, "", False


@callback(
    Output("chat-store", "data", allow_duplicate=True),
    Input("chat-submit", "n_clicks"),
    State("chat-input", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True,
)
def on_send(n, user_text, chat_hist):
    """Send typed message to OpenAI and append assistant reply."""
    chat_hist = chat_hist or []
    if not user_text:
        return chat_hist

    # user message
    chat_hist.append({"role": "user", "content": user_text})

    # assistant reply
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant for glider mission file conversion."}] + chat_hist
        )
        assistant_msg = resp.choices[0].message.content
        chat_hist.append({"role": "assistant", "content": assistant_msg})
    except Exception as e:
        chat_hist.append({"role": "assistant", "content": f"Error: {e}"})

    return chat_hist


@callback(
    Output("chat-output", "children"),
    Input("chat-store", "data"),
)
def render_chat(history):
    if not history:
        return [html.Div("Start by dropping a .mi/.ma file or typing a message above.")]

    rendered = []
    for msg in history:
        if msg["role"] == "assistant":
            rendered.append(
                html.Div(
                    [
                        html.B("Assistant:"),
                        dcc.Markdown(
                            msg["content"],
                            link_target="_blank",
                            style={"marginTop": "6px"}
                        )
                    ],
                    style={
                        "marginBottom": "12px",
                        "padding": "8px",
                        "borderRadius": "6px",
                        "backgroundColor": "#f4f8ff",
                        "border": "1px solid #e0e6f0"
                    }
                )
            )
        elif msg["role"] == "user":
            rendered.append(
                html.Div(
                    [
                        html.B("You: "),
                        html.Pre(msg["content"], style={"whiteSpace": "pre-wrap"})
                    ],
                    style={
                        "marginBottom": "12px",
                        "padding": "8px",
                        "borderRadius": "6px",
                        "backgroundColor": "#ffffff",
                        "border": "1px solid #e5e5e5"
                    }
                )
            )
    return rendered



@callback(
    Output("mi-files-store-view", "children"),
    Input("mi-files-store", "data"),
)
def render_mi_files(items):
    if not items:
        return html.Div("No .mi files uploaded yet.", style={"color": "#666"})
    blocks = []
    for rec in items:
        blocks.append(
            html.Div(
                [
                    html.Div(html.B(rec["name"]), style={"marginBottom": "4px"}),
                    html.Pre(short_preview(rec["content"], limit=1500)),
                    html.Hr(),
                ]
            )
        )
    return blocks


@callback(
    Output("ma-files-store-view", "children"),
    Input("ma-files-store", "data"),
)
def render_ma_files(items):
    if not items:
        return html.Div("No .ma files uploaded yet.", style={"color": "#666"})
    blocks = []
    for rec in items:
        blocks.append(
            html.Div(
                [
                    html.Div(html.B(rec["name"]), style={"marginBottom": "4px"}),
                    html.Pre(short_preview(rec["content"], limit=1500)),
                    html.Hr(),
                ]
            )
        )
    return blocks
