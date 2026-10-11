*** Settings ***
Documentation  Search with an implicit wildcard (F12), livesearch (F13).
...            Version-independent: Plone selectors are in ui_plone*.robot.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
A search for the beginning of a word finds the document
    Log in as the manager
    Go to  ${PLONE_URL}
    Search with the search box  Corresp
    The search results contain  ${DOC_TITLE}

A tag link lists the tagged content
    [Documentation]  Plone 4 bug: the implicit wildcard turns a search without text into SearchableText=*,
    ...              which finds nothing.
    [Tags]  plone4-bug
    Log in as the manager
    Go to  ${DOC_URL}
    Click the tag  mail
    The search results contain  ${DOC_TITLE}

Livesearch shows the state of the results and a link to the advanced search
    [Documentation]  Plone 6 has another livesearch: the port may drop this override.
    [Tags]  plone4-only
    Log in as the manager
    Go to  ${PLONE_URL}
    Type in the search box  Corresp
    The livesearch shows  ${DOC_TITLE}  private
    The livesearch links to the advanced search  Corresp
