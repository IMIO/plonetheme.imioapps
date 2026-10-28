*** Settings ***
Documentation  Help icon (F9). Version-independent.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Variables ***
${HELP_URL}  https://docs.imio.be/iadocs


*** Test Cases ***
Without a help URL there is no help icon
    Log in as the manager
    Go to  ${DOC_URL}
    The help icon is not shown

The help icon links to the configured help URL
    Set help url  ${HELP_URL}
    Log in as the manager
    Go to  ${DOC_URL}
    The help icon links to  ${HELP_URL}
