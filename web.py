from web import arguments
from runner import run


args = arguments.parse_arg()
project = 'web'
run(project, args)
