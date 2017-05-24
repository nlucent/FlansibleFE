WTF_CSRF_ENABLED = True
SECRET_KEY = 'asdlfkjboien34jnfboi34u3io4jg'

PB_POST_URL = 'http://10.9.26.174:3000/api/ansibleplaybook'
PB_POST_USER = 'admin'
PB_POST_PASSWD = 'admin'
PBSTATUS_URL = 'http://10.9.26.174:3000/api/ansibletaskoutput/'
PLAYBOOKS = {
	'playbook_1': {
		'path': '/path/to/some/playbook',
		'desc': 'Some thing that does something',
		'extra_vars': [ 'var1', 'var2', 'var3', 'var4'],
	},
	'playbook_2': {
		'path': '/path/to/some/playbook2',
		'desc': 'Some other thing that does some other thing',
		'extra_vars': [ 'var4', 'var5', 'var6', 'var7'],
	},
	'FlansibleHelloWorld': {
		'path': '/home/nlucent/flansible/playbook',
		'desc': 'Hello world FlansibleFE Test playbook',
		'extra_vars': ['hosts', 'path', 'content'],
	},
	'InstallFlansibleFE': {
		'path': '/home/nlucent/flansible/playbook',
		'desc': 'Install and configure Flansible + FlansibleFE',
		'extra_vars': ['host', 'flansible_basedir', 'flansiblefe_basedir', 'anaconda_dir']
	}

}