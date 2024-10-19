import argparse
import yaml

parser = argparse.ArgumentParser(prog='make_stack.py',
                                 description='Build Docker stacks for different numbers of SITL rover')
parser.add_argument('-n','--number',help='Number of rovers to be simulated',default=5)
args=parser.parse_args()

num_rovers = int(args.number)
print(f'Making stack for {num_rovers} rovers...')

compose_dict = {"version": "3.8",
                "services":
                    {"mavgw":{"image":"mickeyli789/mavlink-router",
                              "volumes":["./app:/app"],
                              "depends_on":[f'rovers_{i+1}' for i in range(num_rovers)],
                              "entrypoint": f"sh /app/gw_launch_{num_rovers}.sh",
                              "ports":["5760:5760"]}}}

for i in range(num_rovers):
    lat = 51.501592+0.0001*i
    lon = -2.551791+0.0001*i
    hdg = 15*i
    compose_dict['services'][f'rovers_{i+1}'] = {"image": "murphy360/ardupilot-sitl-rover",
                                                 "entrypoint": f"/ardupilot/build/sitl/bin/apmrover2 -w --model=rover --home={lat},{lon},0,{hdg} --defaults /ardupilot/Tools/autotest/default_params/copter.parm --sysid={i+1}"}

with open(f'docker-compose-{num_rovers}.yml', 'w', encoding='utf8') as file:
    yaml.dump(compose_dict, file)

router_cmds = ['/mavlink-router/mavlink-routerd -c NULL'] + [f"-p $(sh /app/get_host_ip.sh rovers_{i+1}):5760" for i in range(num_rovers)]                                    

with open(f'app/gw_launch_{num_rovers}.sh', 'w', newline="\n", encoding='utf8') as file:
    file.write("#!/bin/sh\n")
    file.write(' '.join(router_cmds))

print('To run type:')
print(f'docker-compose -f docker-compose-{num_rovers}.yml up')
print('or:')
print(f'docker stack deploy --compose-file docker-compose-{num_rovers}.yml rovers_{num_rovers}')