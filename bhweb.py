#!/usr/bin/env python2.7

import sys, argparse, json, os, urllib2, ConfigParser
from flask import Flask, render_template, url_for, send_from_directory

parser = argparse.ArgumentParser(description='This is a genuine frontend for bithorded deamon.')
parser.add_argument('--bithorded-config', type=str, default='/etc/bithorde.conf', help='Read bithorded configuration file (default: /etc/bithorde.conf)')
parser.add_argument('--port', type=str, default=1447, help='Bind to port (default: 1447)')
parser.add_argument('--interface-ip', type=str, default='0.0.0.0', help='Bind to ip (default: all interfaces)')

args = parser.parse_args()

web = Flask(__name__, static_url_path='')
web.jinja_env.trim_blocks = True
web.jinja_env.lstrip_blocks = True

class base():
  def __init__(self):
    self.test = 0
    self.Config = ConfigParser.ConfigParser()
    self.version = '0.1'

  def readconfig(self):
    try:
      self.Config.read(args.bithorded_config)
    except:
      print('Config file '+args.bithorded_config+' does not exist or is not readable.')
      sys.exit(1)
    self.configsections = self.Config.sections()
    self.configdata = {}
    for section in self.configsections:
      self.configdata[section] = {}      
      for option in self.Config.options(section):
        self.configdata[section][option] = self.Config.get(section, option)

  def readinspect(self):
    self.readconfig()
    self.configdata['server']['inspectport']
    reqroot = urllib2.Request('http://localhost:'+self.configdata['server']['inspectport'], headers={"Accept" : "application/json"})
    reqrouter = urllib2.Request('http://localhost:'+self.configdata['server']['inspectport']+'/router', headers={"Accept" : "application/json"})
    reqconnections = urllib2.Request('http://localhost:'+self.configdata['server']['inspectport']+'/connections', headers={"Accept" : "application/json"})
    self.insproot = json.load(urllib2.urlopen(reqroot))
    self.insprouter = json.load(urllib2.urlopen(reqrouter))
    self.inspconnections = json.load(urllib2.urlopen(reqconnections))

@web.route('/', methods=['GET'])
def status():
  title = 'Status'
  bhweb = base()
  bhweb.readinspect()
  return render_template('status.html', title=title, bhweb=bhweb)

@web.route('/settings', methods=['GET'])
def settings():
  title = 'Settings'
  bhweb = base()
  bhweb.readconfig()
  return render_template('settings.html', title=title, bhweb=bhweb)

@web.route('/friends', methods=['GET'])
def friends():
  title = 'Friends'
  bhweb = base()
  bhweb.readconfig()
  return render_template('friends.html', title=title, bhweb=bhweb)

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
    web.run(host=args.interface_ip, port=int(args.port))
