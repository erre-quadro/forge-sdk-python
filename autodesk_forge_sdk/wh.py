from typing import Dict, Tuple, Union
from autodesk_forge_sdk.auth import Scope, TokenProviderInterface
from autodesk_forge_sdk.client import ForgeClient, Region
from enum import Enum


BASE_URL = "https://developer.api.autodesk.com/webhooks/v1"


class Status(str, Enum):
    active = "active"
    inactive = "inactive"


class Sort(str, Enum):
    asc = "asc"
    desc = "desc"


class DataManagementEvent(str, Enum):
    version_added = "dm.version.added"
    version_modified = "dm.version.modified"
    version_deleted = "dm.version.deleted"
    version_moved = "dm.version.moved"
    version_moved_out = "dm.version.moved.out"
    version_copied = "dm.version.copied"
    lineage_reserved = "dm.lineage.reserved"
    lineage_unreserved = "dm.lineage.unreserved"
    lineage_updated = "dm.lineage.updated"
    folder_added = "dm.folder.added"
    folder_modified = "dm.folder.modified"
    folder_deleted = "dm.folder.deleted"
    folder_moved = "dm.folder.moved"
    folder_copied = "dm.folder.copied"
    operation_started = "dm.operation.started"
    operation_completed = "dm.operation.completed"


class ModelDerivativeEvent(str, Enum):
    extraction_finished = "extraction.finished"
    extraction_updated = "extraction.updated"


Event = Union[DataManagementEvent, ModelDerivativeEvent]


class WebhooksClient(ForgeClient):
    """
    Forge Webhooks service client.

    **Documentation**: https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/
    """

    def __init__(
        self, token_provider: TokenProviderInterface, base_url: str = BASE_URL
    ):
        """
        Create new instance of the client.

        Args:
            token_provider (autodesk_forge_sdk.auth.TokenProviderInterface):
                Provider that will be used to generate access tokens for API calls.

                Use `autodesk_forge_sdk.auth.OAuthTokenProvider` if you have your app's client ID
                and client secret available, `autodesk_forge_sdk.auth.SimpleTokenProvider`
                if you would like to use an existing access token instead, or even your own
                implementation of the `autodesk_forge_sdk.auth.TokenProviderInterface` interface.
            base_url (str, optional): Base URL for API calls.

        Examples:
            ```
            FORGE_CLIENT_ID = os.environ["FORGE_CLIENT_ID"]
            FORGE_CLIENT_SECRET = os.environ["FORGE_CLIENT_SECRET"]
            client1 = WebhooksClient(
                OAuthTokenProvider(FORGE_CLIENT_ID, FORGE_CLIENT_SECRET))

            FORGE_ACCESS_TOKEN = os.environ["FORGE_ACCESS_TOKEN"]
            client2 = WebhooksClient(SimpleTokenProvider(FORGE_ACCESS_TOKEN))

            class MyTokenProvider(autodesk_forge_sdk.auth.TokenProviderInterface):
                def get_token(self, scopes):
                    return "your own access token retrieved from wherever"
            client3 = WebhooksClient(MyTokenProvider())
            ```
        """
        ForgeClient.__init__(self, token_provider, base_url)

    async def get_hook(
        self, system: str, event: Event, hook_id: str, region: Region = Region.US
    ) -> Dict:
        """
        Get details of a webhook based on its webhook ID.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-hook_id-GET/)

        Args:
            system (str): A system for example: **data** for Data Management.
            event (Event): Type of event. See [Supported Events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events).
            hook_id (str): Id of the webhook to retrieve.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix({"region": region})
        return await self._req_json(
            self._get,
            f"/systems/{system}/events/{event}/hooks/{hook_id}",
            params=params,
            scopes=[Scope.DATA_READ],
        )

    async def get_event_hooks(
        self,
        system: str,
        event: Event,
        scope_name: str = None,
        scope_value: str = None,
        page_state: str = None,
        status: Status = Status.active,
        region: Region = Region.US,
    ) -> Dict:
        """
        Retrieves a paginated list of all the webhooks for a specified event.
        If the pageState query string is not specified, the first page is returned.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-GET/)

        Args:
            system (str): A system for example: **data** for Data Management.
            event (Event): Type of event. See [Supported Events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events).
            scope_name (str): Scope name used to create hook. For example: folder.
            scope_value (str): Scope value used to create hook.
                If scope_value is present then scope_name must be present, otherwise scope_value would be ignored.
            page_state (str): Base64 encoded string used to return the next page of the list of webhooks.
                This can be obtained from the next field of the previous page.
                PagingState instances are not portable and implementation is subject to change across versions.
                Default page size is 200.
            status (Status): Status of the hooks. Options: ```Status.active```, ```Status.inactive```.
                Default is ```Status.active```.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix(
            {
                "scopeName": scope_name,
                "scopeValue": scope_value,
                "pageState": page_state,
                "status": status,
                "region": region,
            }
        )
        return await self._req_json(
            self._get,
            f"/systems/{system}/events/{event}/hooks",
            params=params,
            scopes=[Scope.DATA_READ],
        )

    async def get_system_hooks(
        self,
        system: str,
        page_state: str = None,
        status: Status = Status.active,
        region: Region = Region.US,
    ) -> Dict:
        """
        Retrieves a paginated list of all the webhooks for a specified system.
        If the pageState query string is not specified, the first page is returned.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-hooks-GET/)

        Args:
            system (str): A system for example: **data** for Data Management.
            page_state (str): Base64 encoded string used to return the next page of the list of webhooks.
                This can be obtained from the next field of the previous page.
                PagingState instances are not portable and implementation is subject to change across versions.
                Default page size is 200.
            status (Status): Status of the hooks. Options: ```Status.active```, ```Status.inactive```.
                Default is ```Status.active```.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix(
            {
                "pageState": page_state,
                "status": status,
                "region": region,
            }
        )
        return await self._req_json(
            self._get,
            f"/systems/{system}/hooks",
            params=params,
            scopes=[Scope.DATA_READ],
        )

    async def get_hooks(
        self,
        page_state: str = None,
        status: Status = Status.active,
        region: Region = Region.US,
    ):
        """
        Retrieves a paginated list of all the webhooks.
        If the pageState query string is not specified, the first page is returned.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/hooks-GET/)

        Args:
            system (str): A system for example: **data** for Data Management.
            page_state (str): Base64 encoded string used to return the next page of the list of webhooks.
                This can be obtained from the next field of the previous page.
                PagingState instances are not portable and implementation is subject to change across versions.
                Default page size is 200.
            status (Status): Status of the hooks. Options: ```Status.active```, ```Status.inactive```.
                Default is ```Status.active```.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix(
            {
                "pageState": page_state,
                "status": status,
                "region": region,
            }
        )
        return await self._req_json(
            self._get, f"/hooks", params=params, scopes=[Scope.DATA_READ]
        )

    async def get_app_hooks(
        self,
        page_state: str = None,
        status: Status = Status.active,
        sort: Sort = Sort.desc,
        region: Region = Region.US,
    ):
        """
        Retrieves a paginated list of webhooks created in the context of a Client or Application.
        This API accepts 2-legged token of the application only.
        If the pageState query string is not specified, the first page is returned.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/app-hooks-GET/)

        Args:
            system (str): A system for example: **data** for Data Management.
            page_state (str): Base64 encoded string used to return the next page of the list of webhooks.
                This can be obtained from the next field of the previous page.
                PagingState instances are not portable and implementation is subject to change across versions.
                Default page size is 200.
            status (Status): Status of the hooks. Options: ```Status.active```, ```Status.inactive```.
                Default is ```Status.active```.
            sort (Sort): Sort order of the hooks based on last updated time.
                Options: ```Sort.asc```, ```Sort.desc```.
                Default is ```Sort.desc```.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix(
            {
                "pageState": page_state,
                "status": status,
                "sort": sort,
                "region": region,
            }
        )
        return await self._req_json(
            self._get, f"/app/hooks", params=params, scopes=[Scope.DATA_READ]
        )

    async def add_hook_for_event(
        self,
        system: str,
        event: Event,
        callback_url: str,
        scope: Dict[str, str],
        region: Region = Region.US,
        hook_attribute: Dict[str, Union[str, int, float]] = None,
        filter: str = None,
        hub_id: str = None,
        project_id: str = None,
        tenant: str = None,
        auto_reactivate_hook: bool = None,
        hook_expiry: str = None,
        callback_with_event_payload_only: bool = None,
    ):
        """
        Add new webhook to receive the notification on a specified event.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-POST/)

        Args:
            system (str): A system for example: **data** for Data Management.
            event (Event): Type of event. See [Supported Events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events).
            callback_url (str): Callback URL registered for the webhook.
            scope (dict): An object that represents the extent to where the event is monitored.
                For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder.
                Please refer to the individual event specification pages for valid scopes.
                For example, [Data Management events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events/data_management_events).
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
            hook_attribute (dict): A user-defined JSON object, which you can use to store/set some custom information.
                The maximum size of the JSON object (content) should be less than 1KB.
            filter (str): JsonPath expression that can be used by you to filter the callbacks you receive.
            hub_id (str): Optional field which should be provided if the user is a member of a large number of projects.
                This hub ID corresponds to an account ID in the BIM 360 API, prefixed by “b.”
            project_id (str): Optional field which should be provided if the user is a member of a large number of projects.
                This project ID corresponds to the project ID in the BIM 360 API, prefixed by “b.”
            tenant (str): The tenant that the event is from.
                If the tenant is specified on the hook, then either the tenant or the scopeValue of the event must match the tenant of the hook.
            auto_reactivate_hook (bool): Optional. Flag to enable the hook for the automatic reactivation flow. See [Event Delivery Guarantees](https://forge.autodesk.com/en/docs/webhooks/v1/developers_guide/event-delivery-guarantees) for more details.
            hook_expiry (str): Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted.
                Not providing this parameter means the hook never expires.
            callback_with_event_payload_only (bool): Optional. If ```True```, the callback request payload only contains the event payload, without additional information on the hook.
                Hook attributes will not be accessible if this is ```True```.
                Defaults to ```False```.
        """
        params = _get_params_fix({"region": region})
        body = _get_params_fix(
            {
                "callbackUrl": callback_url,
                "scope": scope,
                "hookAttribute": hook_attribute,
                "filter": filter,
                "hubId": hub_id,
                "projectId": project_id,
                "tenant": tenant,
                "autoReactivateHook": auto_reactivate_hook,
                "hookExpiry": hook_expiry,
                "callbackWithEventPayloadOnly": callback_with_event_payload_only,
            }
        )
        await self._post(
            f"/systems/{system}/events/{event}/hooks",
            params=params,
            json=body,
            scopes=[Scope.DATA_READ, Scope.DATA_WRITE],
        )

    async def add_hook_for_system(
        self,
        system: str,
        callback_url: str,
        scope: Dict[str, str],
        region: Region = Region.US,
        hook_attribute: Dict[str, Union[str, int, float]] = None,
        filter: str = None,
        hub_id: str = None,
        project_id: str = None,
        tenant: str = None,
        auto_reactivate_hook: bool = None,
        hook_expiry: str = None,
        callback_with_event_payload_only: bool = None,
    ):
        """
        Add new webhook to receive the notification on a specified event.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-POST/)

        Args:
            system (str): A system for example: **data** for Data Management.
            callback_url (str): Callback URL registered for the webhook.
            scope (dict): An object that represents the extent to where the event is monitored.
                For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder.
                Please refer to the individual event specification pages for valid scopes.
                For example, [Data Management events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events/data_management).
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
            hook_attribute (dict): A user-defined JSON object, which you can use to store/set some custom information.
                The maximum size of the JSON object (content) should be less than 1KB.
            filter (str): JsonPath expression that can be used by you to filter the callbacks you receive.
            hub_id (str): Optional field which should be provided if the user is a member of a large number of projects.
                This hub ID corresponds to an account ID in the BIM 360 API, prefixed by “b.”
            project_id (str): Optional field which should be provided if the user is a member of a large number of projects.
                This project ID corresponds to the project ID in the BIM 360 API, prefixed by “b.”
            tenant (str): The tenant that the event is from.
                If the tenant is specified on the hook, then either the tenant or the scopeValue of the event must match the tenant of the hook.
            auto_reactivate_hook (bool): Optional. Flag to enable the hook for the automatic reactivation flow. See [Event Delivery Guarantees](https://forge.autodesk.com/en/docs/webhooks/v1/developers_guide/event-delivery-guarantees) for more details.
            hook_expiry (str): Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted.
                Not providing this parameter means the hook never expires.
            callback_with_event_payload_only (bool): Optional. If ```True```, the callback request payload only contains the event payload, without additional information on the hook.
                Hook attributes will not be accessible if this is ```True```.
                Defaults to ```False```.
        """
        params = _get_params_fix({"region": region})
        body = _get_params_fix(
            {
                "callbackUrl": callback_url,
                "scope": scope,
                "hookAttribute": hook_attribute,
                "filter": filter,
                "hubId": hub_id,
                "projectId": project_id,
                "tenant": tenant,
                "autoReactiveHook": auto_reactivate_hook,
                "hookExpiry": hook_expiry,
                "callbackWithEventPayloadOnly": callback_with_event_payload_only,
            }
        )
        await self._post(
            f"/systems/{system}/hooks",
            params=params,
            json=body,
            scopes=[Scope.DATA_READ, Scope.DATA_WRITE],
        )

    async def update_hook(
        self,
        system: str,
        event: Event,
        hook_id: str,
        status: Status,
        region: Region = Region.US,
        filter: str = None,
        hook_attribute: Dict[str, Union[str, int, float]] = None,
        token: str = None,
        auto_reactivate_hook: bool = None,
        hook_expiry: str = None,
    ):
        """
        Partially update a webhook based on its webhook ID.
        The only fields that may be updated are: status, filter, hookAttribute, and hookExpiry.

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-hook_id-PATCH/)

        Args:
            system (str): A system for example: **data** for Data Management.
            event (Event): Type of event. See [Supported Events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events).
            hook_id (str): Id of the webhook to modify.
            status (Status): Status of the hooks. Options: ```Status.active```, ```Status.inactive```.
                Default is ```Status.active```.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
            filter (str): JsonPath expression that can be used by you to filter the callbacks you receive.
            hook_attribute (dict): A user-defined JSON object, which you can use to store/set some custom information.
                The maximum size of the JSON object (content) should be less than 1KB.
            token (str): A secret token that is used to generate a hash signature, which is passed along with notification requests to the callback URL.
            auto_reactivate_hook (bool): Optional. Flag to enable the hook for the automatic reactivation flow. See [Event Delivery Guarantees](https://forge.autodesk.com/en/docs/webhooks/v1/developers_guide/event-delivery-guarantees) for more details.
            hook_expiry (str): Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted.
                Not providing this parameter means the hook never expires.
        """
        params = _get_params_fix({"region": region})
        body = _get_params_fix(
            {
                "status": status,
                "hookAttribute": hook_attribute,
                "filter": filter,
                "autoReactiveHook": auto_reactivate_hook,
                "hookExpiry": hook_expiry,
                "token": token,
            }
        )
        await self._patch(
            f"/systems/{system}/events/{event}/hooks/{hook_id}",
            params=params,
            json=body,
            scopes=[Scope.DATA_READ, Scope.DATA_WRITE],
        )

    async def delete_hook(
        self,
        system: str,
        event: Event,
        hook_id: str,
        region: Region = Region.US,
    ):
        """
        Deletes a webhook based on webhook ID

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/systems-system-events-event-hooks-hook_id-DELETE/)

        Args:
            system (str): A system for example: **data** for Data Management.
            event (Event): Type of event. See [Supported Events](https://forge.autodesk.com/en/docs/webhooks/v1/reference/events).
            hook_id (str): Id of the webhook to modify.
            region (Region): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix({"region": region})
        await self._delete(
            f"/systems/{system}/events/{event}/hooks/{hook_id}",
            params=params,
            scopes=[Scope.DATA_READ, Scope.DATA_WRITE],
        )

    async def add_token(
        self,
        token: str,
        region: Region = Region.US,
    ):
        """
        Add a new Webhook secret token

        [Documentation](https://forge.autodesk.com/en/docs/webhooks/v1/reference/http/tokens-POST/)

        Args:
            token (str): A secret token that is used to generate a hash signature, which is passed along with notification requests to the callback URL.
            region (str): Specifies the geographical location (region) of the server that the request is executed on.
                Supported values are: ```Region.EMEA```, ```Region.US```.
                Default is ```Region.US```.
        """
        params = _get_params_fix({"region": region})
        await self._post(
            f"/tokens",
            params=params,
            json={"token": token},
            scopes=[Scope.DATA_READ, Scope.DATA_WRITE],
        )


def _get_params_fix(fix_map):
    if isinstance(fix_map, Tuple):
        fix_map = dict(fix_map)
    params = {}
    for k, v in fix_map.items():
        if v is None:
            continue
        if isinstance(v, Enum):
            v = v.value
        params[k] = v
    return params
