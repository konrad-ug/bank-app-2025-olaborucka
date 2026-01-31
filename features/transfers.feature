Feature: Money Transfers

  Scenario: Incoming transfer increases balance
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    When I make a transfer of "100" type "incoming" to account with pesel "12345678901"
    Then Account with pesel "12345678901" has balance equal to "100"

  Scenario: Outgoing transfer decreases balance
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    And I make a transfer of "1000" type "incoming" to account with pesel "12345678901"
    When I make a transfer of "400" type "outgoing" to account with pesel "12345678901"
    Then Account with pesel "12345678901" has balance equal to "600"

  Scenario: Express transfer decreases balance by amount and 1 PLN fee
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    And I make a transfer of "200" type "incoming" to account with pesel "12345678901"
    When I make a transfer of "100" type "express" to account with pesel "12345678901"
    Then Account with pesel "12345678901" has balance equal to "99"

  Scenario: Outgoing transfer fails when funds are insufficient
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    When I make a transfer of "100" type "outgoing" to account with pesel "12345678901" and expect status "422"
    Then Account with pesel "12345678901" has balance equal to "0"

  Scenario: Transfer with invalid type returns 400
    Given Account registry is empty
    And I create an account using name: "Jan", last name: "Kowalski", pesel: "12345678901"
    When I make a transfer of "100" type "kradziez" to account with pesel "12345678901" and expect status "400"

