"""
Clients for communicating with different Autodesk Forge services.
"""

from .auth import AuthenticationClient, Scope, get_authorization_url
from .auth import TokenProviderInterface, SimpleTokenProvider, OAuthTokenProvider
from .dm import OSSClient, ProjectManagementClient, DataManagementClient
from .md import ModelDerivativeClient, urnify
from .wh import DataManagementEvent, ModelDerivativeEvent, WebhooksClient