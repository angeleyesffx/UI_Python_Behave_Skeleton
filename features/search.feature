Feature: Search

  Scenario Outline: Search the terms on Google
    Given I navigate to the Google Home page
    When I search for <data>
    Then I should see the results

    Examples:
        | data          |
        | python        |
        | apples        |