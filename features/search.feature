Feature: Search
  As a web surfer,
  I want to find information online,
  So I can learn new things and get tasks done.

  Background:
    Given I navigate to the Google Home page

  Scenario Outline: Search the terms on Google
    When I search for <data>
    Then I should see the results

    Examples:
        | data          |
        | python        |
        | ruby          |