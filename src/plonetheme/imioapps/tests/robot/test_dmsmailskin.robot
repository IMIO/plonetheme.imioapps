*** Settings ***
Documentation  dmsmailskin, the skin of iA.Docs (F15 logo, F18). Layer DMS_ACCEPTANCE.
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
The dmsmail skin shows its own logo
    Go to  ${PLONE_URL}
    The site logo size is  42  32

The dmsmail skin hides the site actions and the colophon
    Go to  ${PLONE_URL}
    The site actions are visible  ${False}
    The colophon is visible  ${False}
