import dash
from dash import Dash, html, Input, Output, callback, page_container
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv


dash.register_page(__name__, path="/", name="Home")
search_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Search Bar", className="mb-3"),

        ]
    )
)

file_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Drop Files", className="mb-3"),

        ]
    )
)

ma_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Ma Files", className="mb-3"),

        ]
    )
)

mi_card = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Mi Files", className="mb-3"),

        ]
    )
)


layout=dbc.Container(
    [
        html.H3("F"),
        dbc.Row(
            [
            dbc.Col(search_card),
            ]
        ),

        dbc.Row(
            [
            dbc.Col(file_card, width=6),
            dbc.Col(ma_card, width=3),
            dbc.Col(mi_card, width=3),
            ],
        )
    ],
    fluid=True
)

