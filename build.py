import os
import sys
import jinja2

PUID = int(os.environ['PUID'])
PGID = int(os.environ['PGID'])

def env_override(value, key):
  return os.getenv(key, value)

env = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'config')))

env.filters['env_override'] = env_override

template = env.get_template('base.yml')
config = template.render()
file = open('config/config.yml', 'w')
file.write(config)
file.close()
os.chown('config/config.yml', PUID, PGID)