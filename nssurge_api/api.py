#!/usr/bin/env python3

# from dataclasses import dataclass
from typing import Iterable, Mapping
from .types import (
    Capability,
    LogLevel,
    OutboundMode,
    Policy,
    PolicyGroup,
    RequestsType,
    Profile,
    Enabled,
    SetModuleStateRequest,
    EvalScriptMockRequest,
    EvalCronScriptRequest,
    Script,
    ChangeDeviceRequest,
    Proxy,
    Policies,
)
from aiohttp import ClientSession, ClientResponse

# class SurgeAPI:
# 	"""
# 	async context manager
# 	"""


# @dataclass
class SurgeAPIClient:
    """
    Surge HTTP API Client
    https://manual.nssurge.com/others/http-api.html
    """

    def __init__(self, endpoint: str = "http://127.0.0.1:9999", api_key: str = "", trust_env: bool = False):
        self.endpoint: str = endpoint
        self.api_key: str = api_key
        # self.trust_env: bool = trust_env
        self.session: ClientSession = ClientSession(trust_env=trust_env)

    # session: ClientSession

    # @classmethod
    # async def create(cls, endpoint, api_key, session):
    # 	return cls(endpoint, api_key, session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    # def __del__(self):
    #     self.session.close()

    async def get(
        self, path, params: Mapping[str, str] | None = None
    ) -> ClientResponse:
        get_headers = {
            "X-Key": self.api_key,
            "Accept": "*/*",
        }
        url = f"{self.endpoint}{path}"
        # async with self.session.get(url, headers=get_headers,
        #                             params=params) as resp:
        #     return await resp.text()
        return await self.session.get(url, headers=get_headers, params=params)

    async def post(self, path, body) -> ClientResponse:
        post_headers = {
            "X-Key": self.api_key,
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        url = f"{self.endpoint}{path}"
        # async with self.session.post(url, headers=post_headers,
        #                              json=body) as resp:
        #     return await resp.text()
        return await self.session.post(url, headers=post_headers, json=body)

    async def get_cap(self, cap: Capability):
        path = f"/v1/features/{cap}"
        return await self.get(path)

    async def set_cap(self, cap: Capability, value: Enabled):
        path = f"/v1/features/{cap}"
        body = {"enabled": value}
        return await self.post(path, body)

    async def get_outbound_mode(self):
        path = "/v1/outbound"
        return await self.get(path)

    async def set_outbound_mode(self, mode: OutboundMode):
        path = "/v1/outbound"
        body = {"mode": mode}
        return await self.post(path, body)

    async def get_global_policy(self):
        path = "/v1/outbound/global"
        return await self.get(path)

    async def set_global_policy(self, policy: Policy):
        path = "/v1/outbound/global"
        body = {"policy": policy}
        return await self.post(path, body)

    async def get_policy(self, policy: Proxy | Policy | None = None):
        if policy is None:
            # GET /v1/policies
            path = "/v1/policies"
            params = {}
        else:
            # GET /v1/policies/detail?policy_name=ProxyNameHere
            # path = f'/v1/policies/detail?policy_name={policy}'
            # use params
            path = "/v1/policies/detail"
            params = {"policy_name": policy}
        return await self.get(path, params)

    async def test_policies(self, proxies: Iterable[Proxy], url: str | None = None):
        path = "/v1/policies/test"
        if url is not None:
            body = {"policy_names": list(proxies), "url": url}
        else:
            body = {"policy_names": list(proxies)}
        return await self.post(path, body)

    async def get_policy_group(self, policy_group: PolicyGroup | None = None):
        if policy_group is None:
            # GET /v1/policy_groups
            path = "/v1/policy_groups"
            params = {}
        else:
            # GET /v1/policy_groups/select?group_name=GroupNameHere
            # path = f'/v1/policy_groups/select?group_name={policy_group}'
            # use params
            path = "/v1/policy_groups/select"
            params = {"group_name": policy_group}
        return await self.get(path, params)

    async def get_policy_group_test_results(self):
        path = "/v1/policy_groups/test_results"
        return await self.get(path)

    async def set_policy_group(self, policy_group: PolicyGroup, policy: Policy):
        path = "/v1/policy_groups/select"
        body = {"group_name": policy_group, "policy": policy}
        return await self.post(path, body)

    async def test_policy_group(self, policy_group: PolicyGroup):
        path = "/v1/policy_groups/test"
        body = {"group_name": policy_group}
        return await self.post(path, body)

    async def get_requests(self, requests_type: RequestsType = RequestsType.recent):
        # GET /v1/requests/recent
        path = f"/v1/requests/{requests_type}"
        return await self.get(path)

    # async def kill_request(self, request_id: int | None = None):
    async def kill_request(self, request_id: int):
        # POST /v1/requests/kill
        # {"id": 100}
        path = "/v1/requests/kill"
        # if request_id is None:
        #     body = {}
        # else:
        # body = {"id": request_id}
        body = {"id": request_id}
        return await self.post(path, body)

    async def get_active_profile(self, mask_password: bool = True):
        # GET /v1/profiles/current?sensitive=0
        path = "/v1/profiles/current"
        if mask_password:
            params = {"sensitive": "0"}
        else:
            params = {}
        return await self.get(path, params=params)

    async def reload_profile(self):
        # POST /v1/profiles/reload
        path = "/v1/profiles/reload"
        return await self.post(path, {})

    async def switch_profile(self, profile_name: Profile):
        # POST /v1/profiles/switch
        # {"name": "Profile2"}
        path = "/v1/profiles/switch"
        body = {"name": profile_name}
        return await self.post(path, body)

    async def get_profiles(self):
        # GET /v1/profiles
        path = "/v1/profiles"
        return await self.get(path)

    async def validate_profile(self, profile_name: Profile):
        # POST /v1/profiles/check
        # {"name": "Profile2"}
        path = "/v1/profiles/check"
        body = {"name": profile_name}
        return await self.post(path, body)

    async def flush_dns(self):
        # POST /v1/dns/flush
        path = "/v1/dns/flush"
        return await self.post(path, {})

    async def get_dns(self):
        # GET /v1/dns
        path = "/v1/dns"
        return await self.get(path)

    async def test_dns(self):
        """Test the DNS delay."""
        # POST /v1/test/dns_delay
        path = "/v1/test/dns_delay"
        return await self.post(path, {})

    async def get_modules(self):
        # /v1/modules
        path = "/v1/modules"
        return await self.get(path)

    async def set_modules(self, config: SetModuleStateRequest):
        """
        POST /v1/modules
        {
            "router.com": false,
            "Google Home Devices": true
        }
        """
        path = "/v1/modules"
        body = config
        return await self.post(path, body)

    async def get_scripts(self):
        # GET /v1/scripting
        path = "/v1/scripting"
        return await self.get(path)

    async def eval_script_mock(self, req: EvalScriptMockRequest):
        """Evaluate a script with a mock environment."""
        # POST /v1/scripting/evaluate
        path = "/v1/scripting/evaluate"
        body = req
        return await self.post(path, body)

    async def eval_cron_script(self, script_name: Script):
        """Evaluate a cron script immediately."""
        # POST /v1/scripting/cron/evaluate
        # {
        #     "script_name": "script1",
        # }
        path = "/v1/scripting/cron/evaluate"
        body: EvalCronScriptRequest = {"script_name": script_name}
        return await self.post(path, body)

    async def get_devices(self):
        # GET /v1/devices
        path = "/v1/devices"
        return await self.get(path)

    async def get_device_icon(self, icon_id):
        """Obtain the icon of a device. You may get the iconID from device.dhcpDevice.icon"""
        # GET /v1/devices/icon?id={iconID}
        # path = f'/v1/devices/icon?id={icon_id}'
        # use params
        path = "/v1/devices/icon"
        params = {"id": icon_id}
        return await self.get(path, params)

    async def change_device(self, req: ChangeDeviceRequest):
        """
        Change the device properties.
        physicalAddress field is required.
        And you may adjust multiple or one property from name, address, and shouldHandledBySurge.
        """
        # POST /v1/devices
        path = "/v1/devices"
        body = req
        return await self.post(path, body)

    async def stop_engine(self):
        """
        Shutdown Surge engine. If Always On is enabled on Surge iOS, the Surge engine will restart.
        """
        # POST /v1/stop
        path = "/v1/stop"
        return await self.post(path, {})

    async def get_events(self):
        """Obtain the content of the event center"""
        # GET /v1/events
        path = "/v1/events"
        return await self.get(path)

    async def get_rules(self):
        """Obtain the list of rules"""
        # GET /v1/rules
        path = "/v1/rules"
        return await self.get(path)

    async def get_traffic(self):
        """Obtain traffic information"""
        # GET /v1/traffic
        path = "/v1/traffic"
        return await self.get(path)

    async def set_log_level(self, log_level: LogLevel):
        """Change the log level for the current session"""
        # POST /v1/log/level
        # {"level": "info"}
        path = "/v1/log/level"
        body = {"level": log_level}
        return await self.post(path, body)


# convert this curl command to aiohttp code
# curl --silent --show-error --location --request GET "${REQUEST_URI}" --header "X-Key: ${SURGE_HTTP_API_KEY}" --header 'Accept: */*'
