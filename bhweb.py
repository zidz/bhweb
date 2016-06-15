#!/usr/bin/env python2.7

import sys, argparse, json, os, urllib, ConfigParser
from flask import Flask, render_template, url_for, send_from_directory

parser = argparse.ArgumentParser(description='This is a genuine frontend for bithorded deamon.')
parser.add_argument('--bithorded-config', type=str, default='/etc/bithorde.conf', help='Read bithorded configuration file (default: /etc/bithorde.conf)')

args = parser.parse_args()


web = Flask(__name__, static_url_path='')
web.jinja_env.trim_blocks = True
web.jinja_env.lstrip_blocks = True

class base():
  def __init__(self):
    self.test = 0
    self.Config = ConfigParser.ConfigParser()

  def readconfig(self):
    self.Config.read(args.bithorded_config)
    self.configsections = self.Config.sections()
    self.configdata = {}
    for section in self.configsections:
      self.configdata[section] = {}      
      for option in self.Config.options(section):
        self.configdata[section][option] = self.Config.get(section, option)

@web.route('/', methods=['GET'])
def status():
  title = 'Status'
  bhweb = base()
  bhweb.readconfig()
  return render_template('status.html', title=title, bhweb=bhweb)

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
