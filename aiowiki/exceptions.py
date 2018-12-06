class PageNotFound(Exception):
    """Exception raised when a page does not exist"""

    pass


class LoginFailure(Exception):
    """Exception raised when a :func:`~aiowiki.Wiki.login` fails"""

    pass


class BadWikiUrl(Exception):
    """Exception raised when the URL of the :class:`~aiowiki.Wiki` is not in the standard Wikimedia API format"""

    pass


class TokenGetError(Exception):
    """Exception raised when the internal acquiring for a token fails"""

    pass


class CreateAccountError(Exception):
    """Exception raised when :func:`~aiowiki.Wiki.create_account` fails"""

    pass


class EditError(Exception):
    """Exception raised when :func:`~aiowiki.Page.edit` fails"""

    pass
