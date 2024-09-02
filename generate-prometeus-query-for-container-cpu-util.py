import docker
import socket
import csv

def get_hostname():
    return socket.gethostname()

def get_list_of_containers_and_pids():
    dockerClient = docker.from_env()
    hostname = get_hostname()
    
    # Open a CSV file to write the data
    with open(f'./stress_test_data/compose_post_scenario/system_cpu_data/container_pids_{hostname}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['hostname', 'container_name', 'pid'])
        pids_list = ""
        for container in dockerClient.containers.list():
            name = container.name
            pid = container.attrs['State']['Pid']
            monitoring = ["cadvisor", "prometheus", "heisenberg"]
            if any(container_name in name for container_name in monitoring):
                continue
            else:
                writer.writerow([hostname, name, pid])
                pids_list = pids_list + f"{pid}|"
                
        # Remove the trailing "|" character from pids_list
        pids_list = pids_list.rstrip('|')
        
        # Generate both Prometheus queries
        cpu_usage_query = generate_prometheus_query(pids_list, "scaph_process_cpu_usage_percentage")
        power_consumption_query = generate_prometheus_query(pids_list, "scaph_process_power_consumption_microwatts") + " / 1000000"

        return cpu_usage_query, power_consumption_query

def generate_prometheus_query(pids_list, metric_name):
    query = f'avg_over_time({metric_name}{{pid=~"<pids>"}}[15s])'
    updated_query = query.replace("<pids>", pids_list)

    return updated_query

if __name__ == "__main__":
    cpu_usage_query, power_consumption_query = get_list_of_containers_and_pids()
    print("CPU Usage Query:")
    print(cpu_usage_query)
    print("\nPower Consumption Query:")
    print(power_consumption_query)
