Feature: Login MyHome
  As an user from MyHome,
  I want to fill the fields with my credentials,
  So I can Sign In on MyHome.

  Background:
    Given I navigate to the Login page

  Scenario Outline: Login MyHome
    When I fill the credentials from <user>
    Then I should see the my home page

    Examples:
        | user          |
        | valid user    |
        | invalid user  |
