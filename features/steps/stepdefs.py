from behave import given, when, then
from hamcrest import assert_that, equal_to

import os
import subprocess
import re

@given('I created an "{virtualec2}" instance for "{system_name}"')
def step_given_i_created_an_ec2_instance_for_system(context, virtualec2, system_name):
    os.chdir('terraform')
    if system_name == 'Oracle':
        result = subprocess.run(['terraform', 'output', 'oracle_dns'], stdout=subprocess.PIPE)
        context.oracle_dns = result.stdout.decode('utf-8')
        context.oracle_dns = context.oracle_dns.strip('\n')
        result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@'+context.oracle_dns, 'sudo docker ps'], stdout=subprocess.PIPE)
        context.remoteDockerOracleResults = result.stdout.decode('utf-8').splitlines()
        result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@' + context.oracle_dns, 'sudo netstat -tulpn'], stdout=subprocess.PIPE)
        context.remoteNetstatOracleResults = result.stdout.decode('utf-8').splitlines()
    if system_name == 'Tomcat':
        result = subprocess.run(['terraform', 'output', 'tomcat_dns'], stdout=subprocess.PIPE)
        context.tomcat_dns = result.stdout.decode('utf-8')
        context.tomcat_dns = context.tomcat_dns.strip('\n')
        result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@' + context.tomcat_dns, 'sudo docker ps'], stdout=subprocess.PIPE)
        context.remoteDockerTomcatResults = result.stdout.decode('utf-8').splitlines()
        result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@' + context.tomcat_dns, 'sudo netstat -tulpn'],stdout=subprocess.PIPE)
        context.remoteNetstatTomcatResults = result.stdout.decode('utf-8').splitlines()
    os.chdir("..")

@then('the "{system_name}" instance should be running "{app}" on port "{port_number}"')
def step_then_the_instance_should_be_running_app_on_port_portnumber(context, system_name, app, port_number):
    on_app_on_port = False
    if system_name == "Oracle":
        for netStatResult in context.remoteNetstatOracleResults:
            if re.match(r'^tcp\d*\s*\d*\s*\d*\s*[0127\\.\\:]+' + port_number + '\s*[0\.\:]+\*\s*LISTEN\s*\d+\/' + app + '.*$', netStatResult, re.M | re.I):
                on_app_on_port = True

    if system_name == "Tomcat":
        for netStatResult in context.remoteNetstatTomcatResults:
            if re.match(r'^tcp\d*\s*\d*\s*\d*\s*[0127\\.\\:]+' + port_number + '\s*[0\.\:]+\*\s*LISTEN\s*\d+\/' + app + '.*$', netStatResult, re.M | re.I):
                on_app_on_port = True

    assert_that(on_app_on_port, equal_to(True))

@then('the "{system_name}" instance should be running image "{docker_image}"')
def step_then_docker_should_be_running_image(context, system_name, docker_image):
    image_correct = False
    if system_name == "Oracle":
        for dockerResult in context.remoteDockerOracleResults:
            if docker_image in dockerResult:
                image_correct = True

    if system_name == "Tomcat":
        for dockerResult in context.remoteDockerTomcatResults:
            if docker_image in dockerResult:
                image_correct = True

    assert_that(image_correct, equal_to(True))

@then('the "{system_name}" instance Docker should be redirecting port "{port_type}" port "{port_from}" to port "{port_to}"')
def step_docker_should_be_redirecting_port_to_port(context, system_name, port_type, port_from, port_to):
    port_redirect_correct = False
    if system_name == "Oracle":
        for dockerResult in context.remoteDockerOracleResults:
            if (port_type in dockerResult) and (port_from in dockerResult) and (port_to in dockerResult):
                port_redirect_correct = True

    if system_name == "Tomcat":
        for dockerResult in context.remoteDockerTomcatResults:
            if (port_type in dockerResult) and (port_from in dockerResult) and (port_to in dockerResult):
                port_redirect_correct = True


    assert_that(port_redirect_correct, equal_to(True))

@then('the "{system_name}" instance inbound port "{port_number}" should be open')
def step_inbound_port_should_be_open(context, system_name, port_number):
    inbound_port_open = False
    if system_name == 'Oracle':
        result = subprocess.run(['nmap', context.oracle_dns, '-p', port_number], stdout=subprocess.PIPE)
        nmapResults = result.stdout.decode('utf-8').splitlines()
        for nmapResult in nmapResults:
            nmapResult = nmapResult.strip('\n')
            if re.match(r'^' + port_number + '.*open.*$', nmapResult, re.M | re.I):
                inbound_port_open = True

    if system_name == 'Tomcat':
        result = subprocess.run(['nmap', context.tomcat_dns, '-p', port_number], stdout=subprocess.PIPE)
        nmapResults = result.stdout.decode('utf-8').splitlines()
        for nmapResult in nmapResults:
            nmapResult = nmapResult.strip('\n')
            if re.match(r'^' + port_number + '.*open.*$', nmapResult, re.M | re.I):
                inbound_port_open = True

    assert_that(inbound_port_open, equal_to(True))
