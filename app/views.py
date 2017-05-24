from flask import render_template, request, url_for, redirect, flash
from app import app
import simplejson as json
import requests

@app.route('/')
@app.route('/index')
def index():
	# Get list of allowed playbooks from conf file
	pbs = app.config['PLAYBOOKS']
	playbooks = []

	for pbname in pbs.keys():
		playbooks.append(pbname)

	#form = PBSelectForm(playbooks)
	title = 'Choose Playbook'

	return render_template('index.j2', title=title, varlist=playbooks)


@app.route('/config', methods=['POST'])
def variables():

	if request.method == "POST":
		curPB = request.form['pbradio']
		# Read variable list from conf file and display inputs for each
		pbVars = app.config['PLAYBOOKS'][curPB]['extra_vars']
		title = 'Enter required variable values'
		return render_template('variables.j2', title=title, curPB=curPB, varlist=pbVars)

@app.route('/doit', methods=['POST'])
def submitPlaybook():
	if request.method == "POST":
		curPB = request.form['playbook']
		varlist = app.config['PLAYBOOKS'][curPB]['extra_vars']
		vars = {}

		# Playbook variables
		for val in varlist:
			vars[val] = request.form[val]

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

		output = {
			'playbook': curPB + ".yml",
			'playbook_dir': app.config['PLAYBOOKS'][curPB]['path'],
			'extra_vars': vars
		}

		if become:
			output['become'] = become
		if forks:
			output['forks'] = forks
		if inventory:
			output['inventory'] = inventory

		posturl = app.config['PB_POST_URL']
		postusr = app.config['PB_POST_USER']
		postpwd = app.config['PB_POST_PASSWD']

		r = requests.post(posturl, auth=(postusr, postpwd), json=output)

		if r.status_code == 200:
			# get task ID from response
			taskid = json.loads(r.text)['task_id']

			status = requests.get(app.config['PBSTATUS_URL'] + taskid)
			return redirect('/status/' + taskid)

		return json.dumps(output)

@app.route('/status/<taskid>')
def get_status(taskid):
	status = requests.get(app.config['PBSTATUS_URL'] + taskid, auth=(app.config['PB_POST_USER'], app.config['PB_POST_PASSWD']))
	return render_template('status.j2', title="Playbook Results", status=status.text)