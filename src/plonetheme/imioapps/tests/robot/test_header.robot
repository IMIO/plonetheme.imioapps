*** Settings ***
Documentation  Fixed header (F4), sticky dashboard table header (F5), test instance highlight (F6).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
The header stays at the top of the window when scrolling a long page
    Log in as the manager
    Go to  ${DOC_URL}
    The content starts below the header
    Make the page longer than the window
    ${top}=  Header position in the window
    Scroll the window to  1000
    ${scrolled_top}=  Header position in the window
    Should be equal  ${scrolled_top}  ${top}

The dashboard table header sticks below the fixed header
    Log in as the manager
    Go to  ${DOC_URL}
    Inject markup  <table class="faceted-table-results"><thead><tr><th>Title</th></tr></thead></table>
    ${height}=  Header height
    ${top}=  Evaluate  ${height} - 1
    Computed style should be  table.faceted-table-results th  position  sticky
    Computed style should be  table.faceted-table-results th  top  ${top}px

A test or acceptance instance has a red header
    Go to  ${DOC_URL}
    The header is red  ${False}
    Pretend the site is served from  https://iadocs.imio-test.be/plone
    The header is red
    Reload page
    Pretend the site is served from  https://iadocs.imio-acceptation.be/plone
    The header is red
    Reload page
    Pretend the site is served from  https://iadocs.imio.be/plone
    The header is red  ${False}
