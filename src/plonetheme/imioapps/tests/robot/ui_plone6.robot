*** Settings ***
Documentation  Plone 6 Classic UI keywords. Same keyword names and arguments as ui_plone4.robot.
...            Robot Framework 3.0 syntax: shared with the Plone 4.3 (Python 2) environment.
...            Asset keywords: selectors checked on Plone 6.1 (collective.contact.contactlist).
...            Theme keywords (below The edit link is not available): checked on Plone 6.2 Classic UI
...            with the Barceloneta Diazo theme (plonetheme.imioapps phase 7): the sticky header is
...            header#content-header + div#mainnavigation-wrapper (navigation bar and search box).
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=.modal-dialog
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
# theme (raw CSS selectors: also used in JavaScript)
${HEADER}  header#content-header
${NAVIGATION}  div#mainnavigation-wrapper
${CONTENT}  div#above-content-wrapper
${LOGO}  a#portal-logo img
# footer portlets, rendered by the Diazo theme in the footer (a value starting with # is a comment)
${SITE_ACTIONS}  [id="portal-footer"] .site-actions
${COLOPHON}  [id="portal-footer"] .colophon
${GLOBAL_MESSAGE}  div#messagesviewlet
${SEARCH_INPUT}  input#searchGadget
${SEARCH_BUTTON}  button.searchButton
${SEARCH_RESULTS}  div#search-results
${LIVESEARCH}  ul.livesearch-results


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login
    # Plone 6.2 pat-validation disables the button of an invalid form: type once the patterns are loaded
    Wait until page contains element  css=body.patterns-loaded
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Wait until page does not contain element  css=#buttons-login.disabled
    Click button  css=#buttons-login
    Wait until page contains element  css=#personaltools-menulink

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions > a
    Wait until element is visible  css=#plone-contentmenu-actions ul
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories > a
    Wait until element is visible  css=#plone-contentmenu-factories ul

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id}  href  ${url}

The personal action is not available
    [Arguments]  ${action_id}
    Page should not contain element  css=#personaltools-${action_id}

The modal is open
    [Documentation]  Overlay (Plone 4) or modal (Plone 6) showing a form
    Wait until element is visible  ${MODAL} form

Modal element
    [Documentation]  Locator of the element with this id inside the modal
    ...              (an argument starting with # would be a robot comment)
    [Arguments]  ${id}
    [Return]  ${MODAL} [id="${id}"]

Save the modal
    Click button  css=.modal-footer #form-buttons-save

Cancel the modal
    Click button  css=.modal-footer #form-buttons-cancel

The modal is closed
    Wait until page does not contain element  ${MODAL}

The status message contains
    [Arguments]  ${text}
    Wait until element contains  css=.portalMessage  ${text}

The page is not an error
    Page should not contain  ${ERROR_PAGE_TEXT}

The page is not found
    Page should contain  ${NOT_FOUND_TEXT}

The edit link is not available
    Page should not contain element  css=#contentview-edit

Element top in the window
    [Documentation]  Top of the element (raw CSS selector) in the window, in pixels
    [Arguments]  ${selector}
    ${top}=  Execute javascript  return Math.round(document.querySelector('${selector}').getBoundingClientRect().top);
    [Return]  ${top}

Element bottom in the window
    [Arguments]  ${selector}
    ${bottom}=  Execute javascript  return Math.round(document.querySelector('${selector}').getBoundingClientRect().bottom);
    [Return]  ${bottom}

Header position in the window
    [Documentation]  Tops of the header and of the navigation bar (both sticky)
    ${header_top}=  Element top in the window  ${HEADER}
    ${navigation_top}=  Element top in the window  ${NAVIGATION}
    [Return]  ${header_top}/${navigation_top}

Header height
    [Documentation]  Header and navigation bar
    ${height}=  Execute javascript
    ...  return document.querySelector('${HEADER}').offsetHeight + document.querySelector('${NAVIGATION}').offsetHeight;
    [Return]  ${height}

Header background colour
    ${colour}=  Execute javascript  return window.getComputedStyle(document.querySelector('${HEADER}')).backgroundColor;
    [Return]  ${colour}

The content starts below the header
    [Documentation]  The page content is not hidden under the (sticky) header and navigation bar
    ${header_bottom}=  Element bottom in the window  ${NAVIGATION}
    ${content_top}=  Element top in the window  ${CONTENT}
    Should be true  ${content_top} >= ${header_bottom}

Pretend the site is served from
    [Documentation]  Changes the canonical URL of the page and runs the theme script (skin.js) again
    ...              (Plone 6: no global highlightTest() function, the check runs when the script loads)
    [Arguments]  ${url}
    Execute javascript  document.querySelector('link[rel="canonical"]').setAttribute('href', '${url}');
    Execute async javascript
    ...  var done = arguments[arguments.length - 1];
    ...  var script = document.createElement('script');
    ...  script.onload = function () { done(); };
    ...  script.src = document.querySelector('script[src*="++plone++plonetheme.imioapps/skin.js"]').src;
    ...  document.head.appendChild(script);

The global message is shown below the header
    [Arguments]  ${text}
    Wait until element is visible  css=${GLOBAL_MESSAGE}
    Element should contain  css=${GLOBAL_MESSAGE}  ${text}
    Page should not contain element  css=${HEADER} ${GLOBAL_MESSAGE}
    Page should not contain element  css=${NAVIGATION} ${GLOBAL_MESSAGE}
    ${header_bottom}=  Element bottom in the window  ${NAVIGATION}
    ${message_top}=  Element top in the window  ${GLOBAL_MESSAGE}
    Should be true  ${message_top} >= ${header_bottom}

Search with the search box
    [Arguments]  ${text}
    Input text  css=${SEARCH_INPUT}  ${text}
    Click element  css=${SEARCH_BUTTON}

Click the tag
    [Documentation]  Link of a tag (keyword) of the content, to the search page
    [Arguments]  ${tag}
    Click link  xpath=//div[contains(@class, "keywords-viewlet")]//a[normalize-space()="${tag}"]

The search results contain
    [Arguments]  ${title}
    Wait until element contains  css=${SEARCH_RESULTS}  ${title}

The site logo size is
    [Documentation]  Natural size of the logo image, in pixels
    [Arguments]  ${width}  ${height}
    Wait until element is visible  css=${LOGO}
    ${size}=  Execute javascript  var img = document.querySelector('${LOGO}'); return img.naturalWidth + 'x' + img.naturalHeight;
    Should be equal  ${size}  ${width}x${height}

The site actions are visible
    [Arguments]  ${expected}=${True}
    Run keyword if  ${expected}  Element should be visible  css=${SITE_ACTIONS}
    ...  ELSE  Page should not contain element  css=${SITE_ACTIONS}

The colophon is visible
    [Arguments]  ${expected}=${True}
    Run keyword if  ${expected}  Element should be visible  css=${COLOPHON}
    ...  ELSE  Page should not contain element  css=${COLOPHON}

Type in the search box
    [Documentation]  Livesearch (results while typing)
    [Arguments]  ${text}
    Input text  css=${SEARCH_INPUT}  ${text}

The livesearch shows
    [Documentation]  Plone 6: the review state id is a class of the result item (not a span).
    ...              Only used by the plone4-only scenario: not run on Plone 6.
    [Arguments]  ${title}  ${state}
    Wait until element is visible  css=${LIVESEARCH} li.${state}
    Element should contain  css=${LIVESEARCH} li.${state}  ${title}

The livesearch links to the advanced search
    [Documentation]  Plone 6: no advanced search link with the terms in Plone's livesearch
    ...              (plone4-only scenario: not run on Plone 6)
    [Arguments]  ${terms}
    Element attribute value should be  css=${LIVESEARCH} a.advanced-search  href
    ...  ${PLONE_URL}/@@search?SearchableText=${terms}&path=/plone
