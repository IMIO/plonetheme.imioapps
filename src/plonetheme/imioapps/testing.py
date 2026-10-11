from collective.messagesviewlet.utils import add_message
from plone import api
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.robotframework.remote import RemoteLibraryLayer
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.robotframework.utils import disableCSRFProtection
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import zope

import collective.messagesviewlet
import plonetheme.imioapps


MANAGER = "manager"
MANAGER_PASSWORD = "manager-secret"
MEMBER = "member"
MEMBER_PASSWORD = "member-secret"
HELP_URL_RECORD = "plonetheme.imioapps.interfaces.IPlonethemeImioappsSettings.help_url"


def create_global_message(text, msg_id="global-message"):
    """Activated collective.messagesviewlet warning message, shown on the whole site."""
    # adopt_roles isn't enough for the workflow guard when anonymous (robot remote call)
    with api.env.adopt_user(username=MANAGER):
        return add_message(msg_id, "Message", text, msg_type="warning", activate=True)


class ImioappsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # z3c.autoinclude doesn't run in test layers
        self.loadZCML(package=collective.messagesviewlet)
        self.loadZCML(package=plonetheme.imioapps, name="testing.zcml")

    def setUpPloneSite(self, portal):
        # installed by iA.Docs: the theme re-registers its viewlet
        applyProfile(portal, "collective.messagesviewlet:default")
        applyProfile(portal, "plonetheme.imioapps:default")
        portal.portal_workflow.setDefaultChain("simple_publication_workflow")
        # a Manager (logs in with the login form) and a plain Member
        portal.acl_users.userFolderAddUser(MANAGER, MANAGER_PASSWORD, ["Manager"], [])
        portal.acl_users.userFolderAddUser(MEMBER, MEMBER_PASSWORD, ["Member"], [])
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory("Folder", "folder", title="Folder")
        portal.folder.invokeFactory(
            "Document", "doc", title="Correspondence", subject=("mail",)
        )
        setRoles(portal, TEST_USER_ID, ["Member"])


class DmsmailskinLayer(PloneSandboxLayer):
    """The skin profile of iA.Docs (imio.dms.mail depends on it)."""

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plonetheme.imioapps:dmsmailskin")


class RemoteKeywords(RemoteLibrary):
    """Robot keywords run in the site (library ${PLONE_URL}/ImioappsRemote)."""

    def add_global_message(self, text):
        """Add an activated warning message shown on the whole site."""
        disableCSRFProtection()  # XML-RPC POST without CSRF token
        create_global_message(text)

    def set_help_url(self, url):
        """Set the URL of the help icon."""
        disableCSRFProtection()
        api.portal.set_registry_record(HELP_URL_RECORD, url)


REMOTE_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(RemoteKeywords,),
    name="plonetheme.imioapps:ImioappsRemote",
)

FIXTURE = ImioappsLayer(name="plonetheme.imioapps:FIXTURE")
DMS_FIXTURE = DmsmailskinLayer(bases=(FIXTURE,), name="plonetheme.imioapps:DMS_FIXTURE")

INTEGRATION = IntegrationTesting(
    bases=(FIXTURE,), name="plonetheme.imioapps:INTEGRATION"
)
FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="plonetheme.imioapps:FUNCTIONAL")
DMS_INTEGRATION = IntegrationTesting(
    bases=(DMS_FIXTURE,), name="plonetheme.imioapps:DMS_INTEGRATION"
)

ACCEPTANCE = FunctionalTesting(
    bases=(
        FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        REMOTE_FIXTURE,
        zope.WSGI_SERVER_FIXTURE,
    ),
    name="plonetheme.imioapps:ACCEPTANCE",
)
DMS_ACCEPTANCE = FunctionalTesting(
    bases=(
        DMS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        REMOTE_FIXTURE,
        zope.WSGI_SERVER_FIXTURE,
    ),
    name="plonetheme.imioapps:DMS_ACCEPTANCE",
)
