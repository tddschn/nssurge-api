#!/usr/bin/env python3

from typing import Literal
from enum import Enum
import sys

# https://peps.python.org/pep-0655/#usage-in-python-3-11
# if python version >= (3, 11):
if sys.version_info >= (3, 11):
    from typing import TypedDict, NotRequired
else:
    from typing_extensions import TypedDict, NotRequired

# Capability = Literal['mitm', 'capture', 'rewrite', 'scripting', 'system_proxy',
#                      'enhanced_mode']
class Capability(str, Enum):
    mitm = "mitm"
    capture = "capture"
    rewrite = "rewrite"
    scripting = "scripting"
    system_proxy = "system_proxy"
    enhanced_mode = "enhanced_mode"


# OutboundMode = Literal['direct', 'proxy', 'rule']


class OutboundMode(str, Enum):
    direct = "direct"
    proxy = "proxy"
    rule = "rule"


Policy = str
PolicyGroup = str
# RequestsType = Literal['recent', 'active']
class RequestsType(str, Enum):
    recent = "recent"
    active = "active"


Profile = str
Module = str
Enabled = bool
Script = str
# LogLevel = Literal['verbose', 'info', 'notify', 'warning']
class LogLevel(str, Enum):
    verbose = "verbose"
    info = "info"
    notify = "notify"
    warning = "warning"


SetModuleStateRequest = dict[Module, Enabled]

Proxy = str
Proxies = list[Proxy]
PolicyGroups = list[PolicyGroup]
# class Policies(TypedDict):
#     proxies: Proxies
#     policy-groups: PolicyGroups
Policies = TypedDict(
    "Policies", {"proxies": Proxies, "policy-groups": PolicyGroups}
)  # return of get polices


# https://peps.python.org/pep-0589/
class EvalScriptMockRequest(TypedDict):
    """
    {
    "script_text": "The content of JS script",
    "mock_type": "cron",
    "timeout": 5
    }
    """

    script_text: str
    mock_type: str
    timeout: int


class EvalCronScriptRequest(TypedDict):
    script_name: Script


class ChangeDeviceRequest(TypedDict):
    """
    {
    "physicalAddress":"F0:9F:C2:00:00:00", (required)
    "name": "Computer",
    "address": "192.168.1.200",
    "shouldHandledBySurge": true
    }
    """

    physicalAddress: str
    name: NotRequired[str]
    address: NotRequired[str]
    shouldHandledBySurge: NotRequired[bool]
