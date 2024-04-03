import os
from flask import Flask, render_template
import pandas as pd
import socket
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import cv2
import numpy as np
from PIL import Image
raspberrypiData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
raspberrypiData.connect(('192.168.11.75', 5000))

app = Flask(__name__, static_folder='./templates/images')
@app.route('/', methods=['GET','POST'])
@app.route('/start', methods=['GET','POST'])

def index():

    text = "こちらFlaskスネーク。応答せよ。"
    while True:
        a = (raspberrypiData.recv(1024).decode('utf-8'))
        print("aa",a)
 