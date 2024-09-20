import argparse
import requests
import json
import time
import subprocess
from datetime import datetime, timedelta, timezone
import os
from requests.utils import quote

def parse_arguments():
    parser = argparse.ArgumentParser(description="Accept arguments")
    parser.add_argument('--app', type=str, required=True, help="Name of the app for which you are running the experiment")
    parser.add_argument('--scenario', type=str, required=True, help="scenario class name: valid values - 'social_network.ComposePostSimulation','social_network.FollowUsersSimulation','bookstore.UserRegistrationSimulation','bookstore.BuyBooksSimulation'")
    parser.add_argument('--ramp_up_duration', type=int, required=True, help="scenario ramp up duration")
    parser.add_argument('--no_of_users', type=int, required=True, help="no of users that are to be ramped up")
    parser.add_argument('--output_folder', type=str, required=True, help="Name of the output folder")    
    return parser.parse_args()


def trigger_github_workflow(token, repo_owner, repo_name, workflow_id, ref, simulation_class, users, duration, csv_file_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/workflows/{workflow_id}/dispatches"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
    }

    payload = {
        "ref": ref,
        "inputs": {
            "simulationClass": simulation_class,
            "users": str(users),        
            "duration": str(duration),
            "csvFileName": csv_file_name
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    return response

def run_system_measurements(output_folder):
    cpu_utilization_command = f"./measure_system_cpu_uttilization.sh {output_folder}/system_cpu_data"
    power_consumption_command = f"./measure_system_power_consumption.sh {output_folder}/power_consumption_data"
    subprocess.Popen(cpu_utilization_command, shell=True)
    subprocess.Popen(power_consumption_command, shell=True)

def wait_until(seconds):
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(seconds=seconds)
    while datetime.now(timezone.utc) < end_time:
        time.sleep(1)

def get_current_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def run_promethues_queries_for_app(app, servers, start_time, end_time, output_folder_path):
    with open('prometheus_queries.json', 'r') as file:
        data = json.load(file)
    
    for server in servers:
        print(f"Processing server: {server}")
        cpu_utilization_query = f"{data[app]['cpu_utilization'][server]}&start={start_time}&end={end_time}&step=15s"
        cpu_utilization_query_url_encoded = quote(cpu_utilization_query, safe='=&')
        cpu_utilization_url = f"http://145.108.225.7:9090/api/v1/query_range?query={cpu_utilization_query_url_encoded}"
        print(f"getting cpu utilization per container for {app} - {server}")
        run_promethues_query(cpu_utilization_url, f"{output_folder_path}/system_cpu_data/per_container_cpu_usage_{server}_{get_current_timestamp()}.json")
        power_consumption_query = f"{data[app]['power_consumption'][server]}&start={start_time}&end={end_time}&step=15s"
        power_consumption_query_url_encoded = quote(power_consumption_query, safe='=&')
        power_consumption_url = f"http://145.108.225.7:9090/api/v1/query_range?query={power_consumption_query_url_encoded}"
        print(f"getting power consumption per container for {app} - {server}")
        run_promethues_query(power_consumption_url, f"{output_folder_path}/power_consumption_data/per_container_power_consumption_{server}_{get_current_timestamp()}.json")

def run_promethues_query(url, output_file):
    response = requests.get(url)
    if response.status_code == 200:
            data = response.json()
            with open(output_file, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"Query result for {output_file} saved successfully.")
    else:
        print(f"Failed to run prometheus query: {url}")
    

if __name__ == "__main__":
    args = parse_arguments()
    app = args.app
    scenario = args.scenario
    ramp_up_duration = args.ramp_up_duration
    no_of_users = args.no_of_users
    output_folder_path = args.output_folder
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    servers = ['gl2','gl5','gl6']
    cool_down_time = 180
    start_time = datetime.now(timezone.utc)
    start_time_in_iso_format = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time = start_time + timedelta(seconds=ramp_up_duration) +timedelta(seconds=cool_down_time + 30)
    end_time_in_iso_format = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    print(start_time_in_iso_format)
    print(end_time_in_iso_format)
    # #GITHUB Personal Access Token (PAT) is stored as a linux environment variable by running : export GITHUB_PAT="<my-token>"
    # #The PAT is retrieved below using the os module
    print(trigger_github_workflow(os.getenv('GITHUB_PAT'),"ishaskul","gatling-simulations-bs-sn","116115030","main",scenario,no_of_users, ramp_up_duration, "all_users.csv"))
    run_system_measurements(output_folder_path)
    time.sleep(5)
    wait_until(ramp_up_duration + cool_down_time)
    run_promethues_queries_for_app(app, servers, start_time_in_iso_format, end_time_in_iso_format, output_folder_path)