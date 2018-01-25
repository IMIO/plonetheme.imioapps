Changelog
=========

2.0.15 (unreleased)
-------------------

- Skin column-two the same way as column-one.  This makes portlets displayed
  on the left or on the right look similar.
  [gbastien]

2.0.14 (2017-12-07)
-------------------

- Only display the `scan` tab on annexes to roles `Manager/MeetingManager`.
  [gbastien]

2.0.13 (2017-11-28)
-------------------

- Set `vertical-align: bottom` for `input` instead `vertical-align: text-top`
  for `label` to align `input` and `label` correctly.
  [gbastien]

2.0.12 (2017-11-24)
-------------------

- Added favicon.
  [sgeulette]
- Skin `input#form-buttons-cancel` the same way `input.standalone` and skin 
  `collective.eeafaceted.batchactions` buttons the same way `imio.actionspanel`
  buttons.
  [gbastien]

2.0.11 (2017-10-05)
-------------------

- Display navigation portlet same way as other portlets.
  [gbastien]
- Display the infos in the CKeditor SCAYT WebSpellChecker popup correctly.
  [gbastien]

2.0.10 (2017-08-30)
-------------------

- Removed styling for class `form.apFormButton` as it was removed from
  imio.actionspanel 1.29+, the add content select now uses the standard
  `apButton` CSS class like other buttons.
  [gbastien]
- Skin portletFooter to align it right.
  [gbastien]

2.0.9 (2017-08-28)
------------------

- Added icon for the store_every_items_decision_as_annex action
  in the plonemeetingskin.
  [gbastien]
- Fixed fieldset/legend top padding.

2.0.8 (2017-06-09)
------------------

- Make <abbr> and <acronym> dotted underline work for every browsers.
  [gbastien]
- Removed useless code about MeetingFile in plonemeetingskin.
  [gbastien]
- Display <th> of table the same way as it is rendered by appy.pod, namely text
  black and grey background.
  [gbastien]

2.0.7 (2017-03-22)
------------------

- Use a brighter blue color for links.
  [gbastien]

2.0.6 (2017-03-14)
------------------

- Highlight the 'lost password?' link in the login_form.
- Style actionspanel select button
- Adapted styles so font-size and line-height are the same while using CKeditor
- Added file imioapps_ckeditor_moonolisa.css.dtml that is enabled when the
  Moono-Lisa skin is selected in CKEditor properties.  This makes it work
  correctly in Chrome and greyed a bit more the selected buttons
- Reduce fieldset padding in form fieldset tabbing

2.0.5 (2017-01-25)
------------------

- Do not use 'float: left;' to move the <legend> tag, it is not working
  anymore with recent versions of Chrome.  Instead use 'position: absolute;'.
  This works in both FF and Chrome and simplify overal CSS.
- Display AT and DX field title bold but selectable contents as normal.
  This is the case for radio buttons, multiple checkboxes, ...

2.0.4 (2016-12-05)
------------------

- Added margin-left for listingBar 'next elements' button or it sticks
  to previous one. This appears until Plone 4.3.8.
- Update pstskin profile (reduce logo, change css)


2.0.3 (2016-06-17)
------------------

- Removed styling for tags <acronym> and <abbr>.
- Optimized icon position on buttons.
- Small fixes for Chrome.


2.0.2 (2016-05-17)
------------------

- Display header correctly for anonymous when portal_tabs are displayed.
- Removed padding-left added by Firefox to input.
- Skin portlet News.


2.0.1 (2016-05-13)
------------------

- Use navBackgroundColor for listingBar hover and select color.
- Make sure broken images are shown in FF.
- Display default faceted widgets (not advanced) the same height.


2.0 (2016-04-19)
----------------

- New layout.


1.2.7 (2016-01-21)
------------------

- Removed 'meetingadvice' icon relevant CSS as it uses a real icon now.
- Define 'height' for search button so it is displayed correctly in Chrome.
- Added left/right padding to collective.messagesviewlet message.
- Limit padding in z3ctable header cells.


1.2.6 (2015-12-03)
------------------

- imioapps : use a bigger spinner.gif and grey page when faceted is locked

1.2.5 (2015-07-14)
------------------

- Several adaptations regarding imio.dashboard integration

1.2.4 (2015-03-18)
------------------
- plonemeetingskin : do not display a contenttype-x icon for type 'MeetingFile' and 'MeetingItem'
- imioapps : skin also listingBar displayed in referencebrowserwidget

1.2.3 (2014-09-23)
------------------
- Added back skins.zcml that register File System Directory Views
- Added profile to go to version 1.2.3 that removes old _templates File System Directory Views

1.2.2 (2014-09-23)
------------------
- Nothing changed yet.

1.2.1 (2014-09-23)
------------------
- Nothing changed yet.

1.2 (2014-09-22)
----------------
- Nothing yet

1.1 (2014-03-07)
----------------
- Adapted styles

1.0 (2014-02-12)
----------------
- First release, added 4 skins : dmsmailskin, imioapps, plonemeetingskin, pstskin
