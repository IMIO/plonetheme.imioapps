*** Settings ***
Documentation  plonetheme.imioapps keywords, built on the ui_plone${PLONE_MAJOR}.robot keywords.
...            Robot Framework 3.0 syntax (shared with the Plone 4.3 environment).
Resource  ui_plone${PLONE_MAJOR}.robot
# Add global message, Set help url (plonetheme.imioapps.testing.RemoteKeywords)
Library  Remote  ${PLONE_URL}/ImioappsRemote  WITH NAME  ImioappsRemote


*** Variables ***
# users and content of plonetheme.imioapps.testing
${MANAGER}  manager
${MANAGER_PASSWORD}  manager-secret
${FOLDER_URL}  ${PLONE_URL}/folder
${DOC_URL}  ${FOLDER_URL}/doc
${DOC_TITLE}  Correspondence
${RED}  rgb(221, 0, 0)


*** Keywords ***
Log in as the manager
    Log in with the login form  ${MANAGER}  ${MANAGER_PASSWORD}

Inject markup
    [Documentation]  Appends HTML (markup rendered by other add-ons) to the page body
    [Arguments]  ${html}
    Execute javascript  document.body.insertAdjacentHTML('beforeend', '${html}');

Make the page longer than the window
    [Documentation]  Spacer at the end of the page content: a sticky header (Plone 6) only sticks within
    ...              its container, and Barceloneta's flex body shrinks an empty div appended to the body
    Execute javascript  document.querySelector('${CONTENT}').insertAdjacentHTML('beforeend', '<div style="height: 3000px"></div>');

Scroll the window to
    [Documentation]  Instant scroll (Bootstrap, in Plone 6, sets scroll-behavior: smooth)
    [Arguments]  ${y}
    Execute javascript  window.scrollTo({top: ${y}, behavior: 'instant'});
    ${scrolled}=  Execute javascript  return window.pageYOffset;
    Should be equal as integers  ${scrolled}  ${y}

Computed style should be
    [Documentation]  Value of a CSS property computed by the browser for the element (raw CSS selector)
    [Arguments]  ${selector}  ${property}  ${expected}
    ${value}=  Execute javascript
    ...  return window.getComputedStyle(document.querySelector("${selector}")).getPropertyValue("${property}");
    Should be equal  ${value}  ${expected}

The header is red
    [Arguments]  ${expected}=${True}
    ${colour}=  Header background colour
    Run keyword if  ${expected}  Should be equal  ${colour}  ${RED}
    ...  ELSE  Should not be equal  ${colour}  ${RED}

The help icon links to
    [Arguments]  ${url}
    Element should be visible  css=a#imioapp-help img
    Element attribute value should be  css=a#imioapp-help  href  ${url}

The help icon is not shown
    Page should not contain element  css=a#imioapp-help
