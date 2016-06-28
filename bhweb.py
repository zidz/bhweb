#!/usr/bin/env python2.7

import sys, argparse, json, os, urllib2, ConfigParser
from flask import Flask, render_template, url_for, send_from_directory, request, redirect

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
    self.version = '0.3rev1'

  def readconfig(self):
    self.Config.read(args.bithorded_config)

  def getconfvalue(self,section,option):
    self.readconfig()
    try:
      value = self.Config.get(section,option)
    except:
      if option == 'inspectport':
        value = '5000'
      else:
        value = 'N/A'
    return value

  def writeconfig(self):
    configfile = open(args.bithorded_config, 'wb')
    try:
      self.Config.write(configfile)
    finally:
      configfile.close()


  def readinspect(self):
    reqroot = urllib2.Request('http://localhost:'+self.getconfvalue('server','inspectport'), headers={"Accept" : "application/json"})
    reqrouter = urllib2.Request('http://localhost:'+self.getconfvalue('server','inspectport')+'/router', headers={"Accept" : "application/json"})
    reqconnections = urllib2.Request('http://localhost:'+self.getconfvalue('server','inspectport')+'/connections', headers={"Accept" : "application/json"})
    try:
      self.insproot = json.load(urllib2.urlopen(reqroot))
      self.insprouter = json.load(urllib2.urlopen(reqrouter))
      self.inspconnections = json.load(urllib2.urlopen(reqconnections))
    except ValueError:
      self.insproot = {'Incompatible Bithorded':'Please upgrade'}
      self.insprouter = {'Incompatible Bithorded':'Please upgrade'}
      self.inspconnections = {'Incompatible Bithorded':'Please upgrade'}

@web.route('/', methods=['GET'])
def status():
  title = 'Status'
  bhweb = base()
  bhweb.readinspect()
  return render_template('status.html', title=title, bhweb=bhweb)

@web.route('/settings', methods=['GET', 'POST'])
def settings():
  title = 'Settings'
  bhweb = base()
  bhweb.readconfig()
  if request.method == 'POST':
    #print(request.form)
    for option in request.form:
      bhweb.Config.set('server',option,request.form[option])
      bhweb.writeconfig()
  return render_template('settings.html', title=title, bhweb=bhweb)

@web.route('/friends', methods=['GET', 'POST'])
def friends():
  title = 'Friends'
  bhweb = base()
  bhweb.readconfig()
  return render_template('friends.html', title=title, bhweb=bhweb)

@web.route('/friends/<path>', methods=['GET', 'POST'])
def configfriend(path):
  title = 'Friend configurator'
  bhweb = base()
  bhweb.readconfig()
  if not bhweb.Config.has_section(path) and path != 'add':
    return redirect(url_for('friends'))
  if request.method == 'POST':
    print(request.form)
    if 'delete' in request.form:
      print('WILL DELETE')
      bhweb.Config.remove_section(path)
      bhweb.writeconfig()
      return redirect(url_for('friends'))
    if path == 'add':
      friendsection = 'friend.'+request.form['addr']
      if bhweb.Config.has_section(friendsection):
        return redirect(url_for('friends'))
      else:
        bhweb.Config.add_section(friendsection)
    else:
      friendsection = path
    for option in request.form:
      if request.form[option]:
        bhweb.Config.set(friendsection,option,request.form[option])
      else:
        if bhweb.Config.has_option(friendsection,option):
          bhweb.Config.remove_option(friendsection,option)
    bhweb.writeconfig()
    return redirect(url_for('friends'))
  return render_template('configfriend.html', title=title, bhweb=bhweb, path=path)

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
