from monitor.collection import arguments
from runner import run


args = arguments.parse_arg()
project = 'monitor'
run(project, args)
