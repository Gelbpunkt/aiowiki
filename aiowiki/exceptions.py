class PageNotFound(Exception):
    """Exception raised when a page does not exist"""

    pass


class LoginFailure(Exception):
    """Exception raised when a :meth:`~aiowiki.Wiki.login` fails"""

    pass


class BadWikiUrl(Exception):
    """Exception raised when the URL of the :meth:`~aiowiki.Wiki` is not in the standard Wikimedia API format"""

    pass


class TokenGetError(Exception):
    """Exception raised when the internal acquiring for a token fails"""

    pass


class CreateAccountError(Exception):
    """Exception raised when :meth:`~aiowiki.Wiki.create_account` fails"""

    pass


class EditError(Exception):
    """Exception raised when :meth:`~aiowiki.Page.edit` fails"""

    pass

class NoSuchUserError(Exception):
    """Exception raised when :meth:`~aiowiki.userrights` fails"""

    pass

class InvalidGroupError(Exception):
    """Exception raised when :meth:`~aiowiki.userrights` fails"""

    pass

class UserRightsNotChangedError(Exception):
    """Exception raised when :meth:`~aiowiki.userrights` fails"""
    
    pass