*** Settings ***
Documentation  Browser body class (F7). Version-independent.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
The page knows it is shown in Firefox
    Go to  ${PLONE_URL}
    Page should contain element  css=body.using-firefox
    Page should not contain element  css=body.using-chrome
