*** Settings ***
Documentation  Theme colours of the markup of other add-ons (F16): workflow state badge
...            (imio.dms.mail viewlets), e-signature session states and signers (imio.esign).
...            The markup is injected: version-independent.
Resource  plonetheme_imioapps.robot
Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***
Workflow states and signers get the theme colours
    Go to  ${DOC_URL}
    Inject markup  <div class="viewlet_workflowstate"><span class="state-to_do">To do</span></div>
    Inject markup  <span class="signer-refused">Refused</span><span class="state-title-errored">Errored</span>
    Computed style should be  .viewlet_workflowstate span.state-to_do  background-color  rgb(0, 0, 255)
    Computed style should be  .viewlet_workflowstate span.state-to_do  color  rgb(255, 255, 255)
    Computed style should be  span.signer-refused  color  rgb(255, 0, 0)
    Computed style should be  span.state-title-errored  color  rgb(255, 165, 0)
