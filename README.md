# DeathStarBench

Open-source benchmark suite for cloud microservices. DeathStarBench includes five end-to-end services, four for cloud systems, and one for cloud-edge systems running on drone swarms. 

## End-to-end Services <img src="microservices_bundle4.png" alt="suite-icon" width="40"/>

* Social Network (released)
* Media Service (released)
* Hotel Reservation (released)
* E-commerce site (in progress)
* Banking System (in progress)
* Drone coordination system (in progress)

## License & Copyright 

DeathStarBench is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 2.

DeathStarBench is being developed by the [SAIL group](http://sail.ece.cornell.edu/) at Cornell University. 

## Publications

More details on the applications and a characterization of their behavior can be found at ["An Open-Source Benchmark Suite for Microservices and Their Hardware-Software Implications for Cloud and Edge Systems"](http://www.csl.cornell.edu/~delimitrou/papers/2019.asplos.microservices.pdf), Y. Gan et al., ASPLOS 2019. 

If you use this benchmark suite in your work, we ask that you please cite the paper above. 


## Beta-testing

If you are interested in joining the beta-testing group for DeathStarBench, send us an email at: <microservices-bench-L@list.cornell.edu>


### Experiment Runner Block Diagram
![Alt text](./images/Experiment_runner.jpg)

### Stress Testing the Bookstore Application using experiment runner

This document outlines the procedure to run a stress test experiment on the Bookstore application deployed on a Docker Swarm cluster.

## Prerequisites
- Ensure you have access to the manager node of your Docker Swarm cluster.
- The Bookstore application repository must be cloned in the home directory.
- Python 3 should be installed on the manager node.

## Running the Experiment

To run the experiment, follow these steps in sequence:

```sh
# Step 1: SSH into the Manager Node
ssh ishas@145.108.225.7

# Step 2: Clone the Bookstore Repository (If Not Already Cloned)
git clone https://github.com/ishaskul/bookstore.git

# Step 3: Navigate to the Project Directory
cd bookstore

# Step 4: Navigate to the Load Testing Folder
cd load_test_experiment

# Step 5: Run the Experiment
nohup python3 run_experiment.py --app bookstore \
    --scenario social_network.ComposePostSimulation \
    --ramp_up_duration 240 \
    --no_of_users 25000 \
    --output_folder ./compose_posts \
    --iterations 10 > experiment.log 2>&1 &
```

### Overview of Replication Package for Experiment Runner
This replication package is structured as follows:

```
    /
    .
    |--- ./load_test_experiment/run_experiment.py                                                   Main source code of the experiment runner for triggering Gatling stress test
    |--- ./load_test_experiment/prometheus_queries.json                                             JSON file that contains the prometheus queries to be executed to capture performance metrics such as CPU Util, Power Consumption
    |--- ./load_test_experiment/measure_system_cpu_uttilization.sh                                  Shell script which profiles the system level cpu utilization using SAR package in linux
    |--- ./load_test_experiment/measure_system_power_consumption.sh                                 Shell script which profiles the system level power consumption using Powerstat package in linux
    |--- ./load_test_experiment/buy_books_final                                                     Profiled data that is used as the actual data against which the performance model is validated
    |--- ./measurement_triggering_api/trigger_system_util_measurement.py                            Simple flash server which exposes a POST API to start profiling system level cpu utilization and power consumption
    |--- ./measurement_triggering_api/measure_resource_utilization.service                          A systemd service to trigger system CPU utilization and power consumption measurements for a specified duration.
```


