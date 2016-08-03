try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description': 'My Project',
	'author': 'kuritan',
	'url': 'URL to get it',
	'download_url': 'Where to download it.',
	'author_email': 'lizi103@hotmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['ex47'],
	'scripts': [],
	'name': 'projectname'
}

setup(**config)