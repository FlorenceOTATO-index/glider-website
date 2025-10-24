import dash
from dash import Dash, html, Input, Output, callback, page_container
import dash_bootstrap_components as dbc
from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv


dash.register_page(__name__, path="/map", name="Map")
layout=dbc.Container([])