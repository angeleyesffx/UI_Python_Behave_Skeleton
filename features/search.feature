Feature: Search

  Scenario: Search Google
    Given I navigate to the Google Home page
    When I search for "blabla"
    Then I should see the results