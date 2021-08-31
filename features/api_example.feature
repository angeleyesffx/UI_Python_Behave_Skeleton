Feature: API EXAMPLE AUTH
  As an user from AUTH,
  I want to create a token with my credentials,
  So I can Sign In on AUTH.

  Background:
    Given I get the endpoint from TokenAPI
  @api
  Scenario: Get Token
    When the request sends POST to the TokenAPI
    And I get the endpoint from HomeAPI
    And the request sends GET to the HomeAPI
    Then I should see the response
