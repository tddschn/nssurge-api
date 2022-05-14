#!/usr/bin/env python3

# from dataclasses import dataclass
from typing import Iterable
from .types import Capability, OutboundMode, Policy, PolicyGroup
import aiohttp
from aiohttp import ClientSession

# class SurgeAPI:
# 	"""
# 	async context manager
# 	"""


# @dataclass
class SurgeAPIClient:

    def __init__(self,
                 endpoint: str = 'http://127.0.0.1:9999',
                 api_key: str = ''):
        self.endpoint: str = endpoint
        self.api_key: str = api_key
        self.session: ClientSession = ClientSession()

    # session: ClientSession

    # @classmethod
    # async def create(cls, endpoint, api_key, session):
    # 	return cls(endpoint, api_key, session)
    # async def __aenter__(self):
    #     self.session = ClientSession()
    #     return self

    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     await self.session.close()
    async def get(self, path):
        get_headers = {
            "X-Key": self.api_key,
            "Accept": "*/*",
        }
        url = f"{self.endpoint}{path}"
        async with self.session.get(url, headers=get_headers) as resp:
            return await resp.text()

    async def post(self, path, body):
        post_headers = {
            "X-Key": self.api_key,
            "Accept": "*/*",
            "Content-Type": "application/json",
        }
        url = f"{self.endpoint}{path}"
        async with self.session.post(url, headers=post_headers,
                                     json=body) as resp:
            return await resp.text()

    async def get_cap(self, cap: Capability):
        path = f"/v1/features/{cap}"
        return await self.get(path)

    async def set_cap(self, cap: Capability, value: bool):
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
        path = '/v1/outbound/global'
        return await self.get(path)
    
    async def set_global_policy(self, policy: Policy):
        path = '/v1/outbound/global'
        body = {"policy": policy}
        return await self.post(path, body)

    async def get_policy(self, policy: Policy | None = None):
        if policy is None:
            # GET /v1/policies
            path = '/v1/policies'
        else:
            # GET /v1/policies/detail?policy_name=ProxyNameHere
            path = f'/v1/policies/detail?policy_name={policy}'
        return await self.get(path)
    
    async def test_policy(self, policies: Iterable[Policy], url: str):
        path = '/v1/policies/test'
        body = {"policy_names": list(policies), "url": url}
        return await self.post(path, body)

    async def get_policy_group(self, policy_group: PolicyGroup | None = None):
        if policy_group is None:
            # GET /v1/policy_groups
            path = '/v1/policy_groups'
        else:
            # GET /v1/policy_groups/select?group_name=GroupNameHere
            path = f'/v1/policy_groups/select?group_name={policy_group}'
        return await self.get(path)
    
    async def get_policy_group_test_results(self):
        path = '/v1/policy_groups/test_results'
        return await self.get(path)



# convert this curl command to aiohttp code
# curl --silent --show-error --location --request GET "${REQUEST_URI}" --header "X-Key: ${SURGE_HTTP_API_KEY}" --header 'Accept: */*'