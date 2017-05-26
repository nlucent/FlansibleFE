from flask import render_template, request, url_for, redirect
from app import app
import simplejson as json
import requests
import re

@app.route('/')
@app.route('/index')
def index():
	# Get list of allowed playbooks from conf file
	pbs = app.config['PLAYBOOKS']
	playbooks = sorted(pbs.keys())
	title = 'Choose Playbook'
	return render_template('index.j2', title=title, varlist=playbooks)


@app.route('/config', methods=['POST'])
def variables():
	curPB = request.form['pbradio']
	# Read variable list from conf file and display inputs for each
	pbVars = app.config['PLAYBOOKS'][curPB]['extra_vars']
	title = 'Enter required variable values'
	return render_template('variables.j2', title=title, curPB=curPB, varlist=pbVars)

@app.route('/doit', methods=['POST'])
def submitPlaybook():
	# selected playbook
	curPB = request.form['playbook']
	# playbook variables
	varlist = app.config['PLAYBOOKS'][curPB]['extra_vars']
	vars = {}

	# Playbook variables
	for val in varlist:
		vars[val] = request.form[val]

	pbmessage = {
		'playbook': curPB + ".yml",
		'playbook_dir': app.config['PLAYBOOKS'][curPB]['path'],
		'extra_vars': vars
	}

	# Runtime variables
	try:
		inventory = request.form['inventory']
	except:
		inventory = None
	try:
		become = request.form['become']
	except:
		become = None
	try:
		forks = request.form['forks']
	except:
		forks = None

	if inventory:
		pbmessage['inventory'] = inventory
	if forks:
		pbmessage['forks'] = forks
	if become:
		pbmessage['become'] = become

	posturl = app.config['PB_POST_URL']
	postusr = app.config['PB_POST_USER']
	postpwd = app.config['PB_POST_PASSWD']

	r = requests.post(posturl, auth=(postusr, postpwd), json=pbmessage)

	if r.status_code == 200:
		# get task ID from response
		taskid = json.loads(r.text)['task_id']
		status = requests.get(app.config['PBSTATUS_URL'] + taskid)
		return redirect('/status/' + taskid)
	# dump message on failure
	return json.dumps(pbmessage)

@app.route('/status/<taskid>')
def get_status(taskid):
	# Proxy and reformat execution status based on task id
	refresh = 10
	title = "Playbook Results"
	status = requests.get(app.config['PBSTATUS_URL'] + taskid, auth=(app.config['PB_POST_USER'], app.config['PB_POST_PASSWD']))
	formatted = re.sub(r"\s+TASK", "<br>TASK", status.text)

	# playbook execution finished
	if "RECAP" in formatted or "ERROR" in formatted:
		# disable refresh in template
		refresh = 1000
	return render_template('status.j2', title=title, status=formatted, refresh=refresh)


	