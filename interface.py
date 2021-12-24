from interface import arguments
from runner import run


args = arguments.parse_arg()
project = 'interface'
run(project, args)
