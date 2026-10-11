*** Settings ***
Documentation  Plone 4.3 keywords. Same keyword names and arguments as ui_plone6.robot.
...            Robot Framework 3.0 syntax (Python 2 environment).
...            Theme keywords (below The edit link is not available): checked on Plone 4.3
...            (plonetheme.imioapps phase 3). Of the asset keywords above, only Log in with the login form is used.
Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Library  Remote  ${PLONE_URL}/RobotRemote


*** Variables ***
${MODAL}  css=div.overlay-ajax
${ERROR_PAGE_TEXT}  there seems to be an error
${NOT_FOUND_TEXT}  This page does not seem to exist
# theme (raw CSS selectors: also used in JavaScript)
${HEADER}  div#portal-header
${CONTENT}  div#portal-columns
${LOGO}  a#portal-logo img
${SITE_ACTIONS}  ul#portal-siteactions
${COLOPHON}  div#portal-colophon
${GLOBAL_MESSAGE}  div#messagesviewlet
${SEARCH_INPUT}  input#searchGadget
${SEARCH_BUTTON}  input.searchButton
${SEARCH_RESULTS}  div#search-results
${LIVESEARCH}  div#LSResult


*** Keywords ***
Log in with the login form
    [Documentation]  Real login (creates the user folder), unlike autologin
    [Arguments]  ${username}  ${password}
    Disable autologin
    Go to  ${PLONE_URL}/login_form
    Input text  css=#__ac_name  ${username}
    Input password  css=#__ac_password  ${password}
    Click button  css=input[name="submit"]
    Wait until page contains element  css=#portal-personaltools

Click the content action
    [Documentation]  Item of the Actions menu (object_buttons), by action id
    [Arguments]  ${action_id}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions-${action_id}
    Click element  css=#plone-contentmenu-actions-${action_id}

The content action is available
    [Arguments]  ${action_id}  ${expected}=${True}
    Click element  css=#plone-contentmenu-actions dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-actions dd.actionMenuContent
    Run keyword if  ${expected}
    ...  Page should contain element  css=#plone-contentmenu-actions-${action_id}
    ...  ELSE  Page should not contain element  css=#plone-contentmenu-actions-${action_id}

Open the add menu
    Click element  css=#plone-contentmenu-factories dt.actionMenuHeader a
    Wait until element is visible  css=#plone-contentmenu-factories dd.actionMenuContent

The personal action links to
    [Documentation]  Item of the user menu (user actions), by action id
    [Arguments]  ${action_id}  ${url}
    Element attribute value should be  css=#personaltools-${action_id} a  href  ${url}

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
    Click button  ${MODAL} #form-buttons-save

Cancel the modal
    Click button  ${MODAL} #form-buttons-cancel

The modal is closed
    Wait until element is not visible  ${MODAL}

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
    ${top}=  Element top in the window  ${HEADER}
    [Return]  ${top}

Header height
    ${height}=  Execute javascript  return document.querySelector('${HEADER}').offsetHeight;
    [Return]  ${height}

Header background colour
    ${colour}=  Execute javascript  return window.getComputedStyle(document.querySelector('${HEADER}')).backgroundColor;
    [Return]  ${colour}

The content starts below the header
    [Documentation]  The page content is not hidden under the (fixed) header
    ${header_bottom}=  Element bottom in the window  ${HEADER}
    ${content_top}=  Element top in the window  ${CONTENT}
    Should be true  ${content_top} >= ${header_bottom}

Pretend the site is served from
    [Documentation]  Changes the canonical URL of the page and runs the theme check of the instance URL
    [Arguments]  ${url}
    Execute javascript  document.querySelector('link[rel="canonical"]').setAttribute('href', '${url}'); highlightTest();

The global message is shown below the header
    [Arguments]  ${text}
    Wait until element is visible  css=${GLOBAL_MESSAGE}
    Element should contain  css=${GLOBAL_MESSAGE}  ${text}
    Page should not contain element  css=${HEADER} ${GLOBAL_MESSAGE}
    ${header_bottom}=  Element bottom in the window  ${HEADER}
    ${message_top}=  Element top in the window  ${GLOBAL_MESSAGE}
    Should be true  ${message_top} >= ${header_bottom}

Search with the search box
    [Arguments]  ${text}
    Input text  css=${SEARCH_INPUT}  ${text}
    Click element  css=${SEARCH_BUTTON}

Click the tag
    [Documentation]  Link of a tag (keyword) of the content, to the search page
    [Arguments]  ${tag}
    Click link  xpath=//a[contains(@class, "link-category") and normalize-space()="${tag}"]

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
    [Arguments]  ${title}  ${state}
    Wait until element is visible  css=${LIVESEARCH} span.state-${state}
    Element should contain  css=${LIVESEARCH} span.state-${state}  ${title}

The livesearch links to the advanced search
    [Documentation]  Bold link to the search page, with the typed terms
    [Arguments]  ${terms}
    Element attribute value should be  css=${LIVESEARCH} a.advanced-search  href
    ...  ${PLONE_URL}/@@search?SearchableText=${terms}&path=/plone
    Element should be visible  css=${LIVESEARCH} a.advanced-search b
    Page should not contain element  css=${LIVESEARCH} a.show-all-items
