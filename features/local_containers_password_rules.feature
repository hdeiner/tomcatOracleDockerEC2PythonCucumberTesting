Feature: UM Portal API - Password Rules

  As a security officer,
  I want to ensure that users choose passwords that are hard to reproduce,
  So that passwords aren't easily compromised.

  Scenario Outline: Conforms to password rules
    Given I want to change my password with the UM Portal on local containers
    When I tell the password rules api that I want to set my new password to "<password>"
    Then the password rules api should tell me "<passwordAdvice>"

    Examples:
      | password                   | passwordAdvice                                             |
      | 12345                      | password must have letters in it                           |
      | password                   | password must have both upper and lower case letters in it |
      | PASSWORD                   | password must have both upper and lower case letters in it |
      | pASSWORD1                  | password must have at least 1 special case character in it |
      | pASSWORD!                  | password must have at least 1 digit in it                  |
      | pW1!                       | password must be at least 8 characters long                |
      | pass Word1!                | password can not have any spaces in it                     |
      | bFihJv!srBChibW4ay#eXEksdh | password OK                                                |


