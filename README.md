Instructions:

You will periodically need to regenerate the Docker images using
```bash
build_and_test_oracle_tomcat_app_in_docker_containers.sh
```
because the Oracle default password times out after a few days

You then need to run the 
```bash
build_and_test_oracle_tomcat_app_in_docker_containers_in_EC2.sh
```
script to produce the EC2 instances into a state where they will be useful together.

