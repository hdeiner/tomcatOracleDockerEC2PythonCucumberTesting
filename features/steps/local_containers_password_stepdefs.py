from behave import given, when, then
from hamcrest import assert_that, equal_to, contains

import requests
import json

@given('I want to change my password with the UM Portal on local containers')
def step_given_i_want_to_change_my_password_with_the_um_portal_on_local_containers(context):
    context.hostname = "localhost"

@given('I test the oracle_tomcat integration on local containers')
def step_given_i_test_the_oracle_tomcat_integration_on_local_containers(context):
    context.hostname = "localhost"
    url = 'http://' + context.hostname + ':8080/passwordAPI/passwordDB'
    context.password_db_response = requests.get(url)

@when('I tell the password strength api that I want to set my new password to "{password}"')
def step_when_i_tell_the_password_strength_api_that_i_want_to_set_my_new_password_to(context, password):
    context.passwordToTest = password

@when('I tell the password rules api that I want to set my new password to "{password}"')
def step_when_i_tell_the_password_rules_api_that_i_want_to_set_my_new_password_to(context, password):
    context.passwordToTest = password

@then('the password strength api should tell me that the password has a strength of "{passwordStrength}"')
def step_then_the_password_strength_api_should_tell_me_that_the_password_has_a_strength_of(context, passwordStrength):
    url = 'http://' + context.hostname + ':8080/passwordAPI/passwordStrength/' + context.passwordToTest
    response = requests.get(url)
    assert_that(json.loads(response.text)['passwordStrength'], equal_to(passwordStrength))

@then('the password rules api should tell me "{passwordRule}"')
def step_then_the_password_rule_api_should_tell_me(context, passwordRule):
    url = 'http://' + context.hostname + ':8080/passwordAPI/passwordRules/' + context.passwordToTest
    response = requests.get(url)
    assert_that(json.loads(response.text)['passwordRules'], equal_to(passwordRule))

@then('the results should include COUNTRY_ID of "{country}" CITY of "{city}" POSTAL_CODE of "{postal_code}" STATE_PROVINCE of "{state_provence}" STREET_ADDRESS of "{street_address}"')
def step_then_the_results_should_include(context, country, city, postal_code, state_provence, street_address):
    response_text = ((context.password_db_response).text).replace('\n', '')
    json_list = json.loads(response_text[1:len(response_text)-1])
    rows = json_list['RESULT_SET']
    found_row = False
    for row in rows:
        if (row["COUNTRY_ID"]==country):
            if (row["CITY"] == city):
                if (row["POSTAL_CODE"] == postal_code):
                    if (row["STATE_PROVINCE"] == state_provence):
                        if (row["STREET_ADDRESS"] == street_address):
                            found_row=True

    assert_that(found_row, equal_to(True))
