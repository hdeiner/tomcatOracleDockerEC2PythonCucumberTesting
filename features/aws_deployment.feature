Feature: Oracle and Tomcat Servers inside an AWS EC2 Instances

  Scenario: Did the Oracle deployment go well?
    Given I created an "AWS EC2" instance for "Oracle"
    Then the "Oracle" instance should be running "docker-proxy" on port "8080"
    And the "Oracle" instance should be running image "howarddeiner/oracletest:release"
    And the "Oracle" instance Docker should be redirecting port "tcp" port "1521" to port "1521"
    And the "Oracle" instance Docker should be redirecting port "tcp" port "8080" to port "8080"
    And the "Oracle" instance inbound port "22" should be open
    And the "Oracle" instance inbound port "1521" should be open
    And the "Oracle" instance inbound port "8080" should be open

  Scenario: Did the Tomcat deployment go well?
    Given I created an "AWS EC2" instance for "Tomcat"
    Then the "Tomcat" instance should be running "docker-proxy" on port "8080"
    And the "Tomcat" instance should be running image "howarddeiner/tomcattest:releaseawsoracle"
    And the "Tomcat" instance Docker should be redirecting port "tcp" port "8080" to port "8080"
    And the "Tomcat" instance inbound port "22" should be open
    And the "Tomcat" instance inbound port "8080" should be open
