Feature: UM Portal API - Demo of Oracle and Tomcat Integration

  Scenario Outline: Oracle and Tomcat Integrate
    Given I test the oracle_tomcat integration on local containers
    Then the results should include COUNTRY_ID of "<COUNTRY_ID>" CITY of "<CITY>" POSTAL_CODE of "<POSTAL_CODE>" STATE_PROVINCE of "<STATE_PROVINCE>" STREET_ADDRESS of "<STREET_ADDRESS>"

    Examples:
      | COUNTRY_ID | CITY            | POSTAL_CODE | STATE_PROVINCE | STREET_ADDRESS    |
      | UK         | Stretford       | 09629850293 | Manchester     | 9702 Chester Road |
      | US         | Seattle         | 98199       | Washington     | 2004 Charade Rd   |
      | US         | South Brunswick | 50090       | New Jersey     | 2007 Zagora St    |


