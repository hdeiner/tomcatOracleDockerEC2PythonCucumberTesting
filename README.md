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

Finally, test the deployments with:
```bash
behave features --summary --junit
```

It should look something like this:
```bash
howarddeiner@ubuntu:~/PycharmProjects/tomcatOracleDockerEC2PythonCucumberTesting$ behave features --summary 
Feature: Oracle and Tomcat Servers inside an AWS EC2 Instances # features/tomcatServer.feature:1

  Scenario: Did the Oracle deployment go well?                                                   # features/tomcatServer.feature:3
    Given I created an "AWS EC2" instance for "Oracle"                                           # features/steps/stepdefs.py:8 1.551s
    Then the "Oracle" instance should be running "docker-proxy" on port "8080"                   # features/steps/stepdefs.py:36 0.001s
    And the "Oracle" instance should be running image "howarddeiner/oracletest:release"          # features/steps/stepdefs.py:55 0.000s
    And the "Oracle" instance Docker should be redirecting port "tcp" port "1521" to port "1521" # features/steps/stepdefs.py:73 0.000s
    And the "Oracle" instance Docker should be redirecting port "tcp" port "8080" to port "8080" # features/steps/stepdefs.py:73 0.000s
    And the "Oracle" instance inbound port "22" should be open                                   # features/steps/stepdefs.py:91 0.119s
    And the "Oracle" instance inbound port "1521" should be open                                 # features/steps/stepdefs.py:91 0.107s
    And the "Oracle" instance inbound port "8080" should be open                                 # features/steps/stepdefs.py:91 0.133s

  Scenario: Did the Tomcat deployment go well?                                                   # features/tomcatServer.feature:13
    Given I created an "AWS EC2" instance for "Tomcat"                                           # features/steps/stepdefs.py:8 1.640s
    Then the "Tomcat" instance should be running "docker-proxy" on port "8080"                   # features/steps/stepdefs.py:36 0.000s
    And the "Tomcat" instance should be running image "howarddeiner/tomcattest:releaseawsoracle" # features/steps/stepdefs.py:55 0.000s
    And the "Tomcat" instance Docker should be redirecting port "tcp" port "8080" to port "8080" # features/steps/stepdefs.py:73 0.000s
    And the "Tomcat" instance inbound port "22" should be open                                   # features/steps/stepdefs.py:91 0.117s
    And the "Tomcat" instance inbound port "8080" should be open                                 # features/steps/stepdefs.py:91 0.120s

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
14 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m3.789s
```

Make sure that you have installed the proper Python modules first, using things such as
```bash
pip install behave --user
pip install PyHamcrest --user
```