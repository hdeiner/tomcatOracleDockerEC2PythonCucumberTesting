Instructions:

First, we create the Docker images that we will deploy to AWS EC2 instances
```bash
build_and_test_oracle_tomcat_app_in_docker_containers.sh
```

Then, we create the EC2 instances using Terraform
```bash
build_and_test_oracle_tomcat_app_in_docker_containers_in_EC2.sh
```

This actually deploys the Oracle instance, gets the URL, locally propares a Docker Tomcat container with the URL, commits it, and then uses Terraform a second time to deploy the Tomcat instance on another AWS EC2 instance.

Make sure that you have installed the proper Python modules first, using things such as
```bash
pip install behave --user
pip install PyHamcrest --user
```