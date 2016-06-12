#!/usr/bin/env python3

import sys, argparse, json, os
from flask import Flask, render_template, url_for, send_from_directory

parser = argparse.ArgumentParser(description='This is a genuine frontend for bithorded deamon.')
parser.add_argument('--future', action="store_true", default=False, help='The future may show if you are patient.')

args = parser.parse_args()

class base():
  def __init__(self):
    test = 0

web = Flask(__name__, static_url_path='')
web.jinja_env.trim_blocks = True
web.jinja_env.lstrip_blocks = True

@web.route('/', methods=['GET'])
def status():
  title = 'Status'
  bhweb = base()
  return render_template('status.html', title=title)

@web.route('/css/<path:path>')
def send_css(path):
  return send_from_directory('css', path)

@web.route('/fonts/<path:path>')
def send_fonts(path):
  return send_from_directory('fonts', path)

@web.route('/js/<path:path>')
def send_js(path):
  return send_from_directory('js', path)

@web.route('/img/<path:path>')
def send_img(path):
  return send_from_directory('img', path)


if __name__ == "__main__":
    web.debug = True
    web.run(host='0.0.0.0', port=1447)
