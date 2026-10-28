*** Settings ***
Documentation  Global messages (collective.messagesviewlet) out of the fixed header (F8).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
A global message is shown between the header and the content
    Add global message  <p>The site will be down tonight</p>
    Log in as the manager
    Go to  ${DOC_URL}
    The global message is shown below the header  The site will be down tonight
