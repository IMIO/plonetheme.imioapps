from collective.messagesviewlet.interfaces import ICollectiveMessagesviewletLayer


class IThemeSpecific(ICollectiveMessagesviewletLayer):
    """Marker interface that defines a Zope browser layer.
       Make it inherits from the collective.messagesviewlet layer so we are able
       to easily redefine the collective.messagesviewlet viewlet.
    """
