from behave import given, when, then
from hamcrest import assert_that, equal_to

import os
import subprocess
import re

@given('I created an "{virtualec2}" instance for "{system_name}"')
def step_given_i_created_an_ec2_instance_for_system(context, virtualec2, system_name):
    os.chdir('terraform')

    if system_name == 'Oracle':
        context.oracle_dns = get_dns_name('oracle_dns')
        context.remoteDockerOracleResults = get_remote_docker_results(context.oracle_dns)
        context.remoteNetstatOracleResults = get_remote_netstat_results(context.oracle_dns)

    if system_name == 'Tomcat':
        context.tomcat_dns = get_dns_name('tomcat_dns')
        context.remoteDockerTomcatResults = get_remote_docker_results(context.tomcat_dns)
        context.remoteNetstatTomcatResults = get_remote_netstat_results(context.tomcat_dns)

    os.chdir("..")

def get_dns_name(terraform_output_name):
    result = subprocess.run(['terraform', 'output', terraform_output_name], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip('\n')

def get_remote_docker_results(dns_name):
    result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@' + dns_name, 'sudo docker ps'],stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').splitlines()

def get_remote_netstat_results(dns_name):
    result = subprocess.run(['/usr/bin/ssh', '-o', 'StrictHostKeyChecking=no', 'ubuntu@' + dns_name, 'sudo netstat -tulpn'],stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8').splitlines()

@then('the "{system_name}" instance should be running "{app}" on port "{port_number}"')
def step_then_the_instance_should_be_running_app_on_port_portnumber(context, system_name, app, port_number):
    on_app_on_port = False
    if system_name == "Oracle":
        on_app_on_port = is_app_on_port(app, port_number, context.remoteNetstatOracleResults)

    if system_name == "Tomcat":
        on_app_on_port = is_app_on_port(app, port_number, context.remoteNetstatTomcatResults)

    assert_that(on_app_on_port, equal_to(True))

def is_app_on_port(app, port, netStatResults):
    app_on_port = False
    for netStatResult in netStatResults:
        if re.match(
                r'^tcp\d*\s*\d*\s*\d*\s*[0127\\.\\:]+' + port + '\s*[0\.\:]+\*\s*LISTEN\s*\d+\/' + app + '.*$', netStatResult, re.M | re.I):
            app_on_port = True
    return app_on_port

@then('the "{system_name}" instance should be running image "{docker_image}"')
def step_then_docker_should_be_running_image(context, system_name, docker_image):
    image_correct = False
    if system_name == "Oracle":
        image_correct = is_correct_docker_image_being_run(docker_image, context.remoteDockerOracleResults)

    if system_name == "Tomcat":
        image_correct = is_correct_docker_image_being_run(docker_image, context.remoteDockerTomcatResults)

    assert_that(image_correct, equal_to(True))

def is_correct_docker_image_being_run(docker_image, dockerImages):
    image_correct = False
    for dockerImage in dockerImages:
        if docker_image in dockerImage:
            image_correct = True
    return image_correct

@then('the "{system_name}" instance Docker should be redirecting port "{port_type}" port "{port_from}" to port "{port_to}"')
def step_docker_should_be_redirecting_port_to_port(context, system_name, port_type, port_from, port_to):
    port_redirect_correct = False
    if system_name == "Oracle":
        port_redirect_correct = is_docker_port_redirect_correct(port_type, port_from, port_to, context.remoteDockerOracleResults)

    if system_name == "Tomcat":
        port_redirect_correct = is_docker_port_redirect_correct(port_type, port_from, port_to, context.remoteDockerTomcatResults)

    assert_that(port_redirect_correct, equal_to(True))

def is_docker_port_redirect_correct(port_type, port_from, port_to, dockerImages):
    port_redirect_correct = False
    for dockerImage in dockerImages:
        if (port_type in dockerImage) and (port_from in dockerImage) and (port_to in dockerImage):
            port_redirect_correct = True
    return port_redirect_correct

@then('the "{system_name}" instance inbound port "{port_number}" should be open')
def step_inbound_port_should_be_open(context, system_name, port_number):
    inbound_port_open = False
    if system_name == 'Oracle':
        inbound_port_open = is_inbound_port_open(context.oracle_dns, port_number)

    if system_name == 'Tomcat':
        inbound_port_open = is_inbound_port_open(context.tomcat_dns, port_number)

    assert_that(inbound_port_open, equal_to(True))

def is_inbound_port_open(dns_name, port_number):
    inbound_port_open = False
    result = subprocess.run(['nmap', dns_name, '-p', port_number], stdout=subprocess.PIPE)
    nmapResults = result.stdout.decode('utf-8').splitlines()
    for nmapResult in nmapResults:
        nmapResult = nmapResult.strip('\n')
        if re.match(r'^' + port_number + '.*open.*$', nmapResult, re.M | re.I):
            inbound_port_open = True
    return inbound_port_open