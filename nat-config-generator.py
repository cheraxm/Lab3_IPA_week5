import yaml
from jinja2 import Environment, FileSystemLoader

with open('data/routers-nat.yml') as f:
    routers = yaml.safe_load(f)['routers']

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('router-nat.j2')

for router in routers:
    config = template.render(router)

    config_filename = f'config/{router["ip"]}-exercise-nat.txt'

    with open(config_filename, 'w') as f:
        f.write(config)
    
    print(f'Generated NAT configuration for {router["name"]} at {config_filename}')