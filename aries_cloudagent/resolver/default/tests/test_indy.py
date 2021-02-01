"""Test IndyDIDResolver."""

import pytest
from asynctest import mock as async_mock

from ..indy import IndyDIDResolver
from ....core.in_memory import InMemoryProfile
from ....core.profile import ProfileSession
from ....ledger.indy import IndySdkLedger
from ....ledger.base import BaseLedger
from ...tests.test_did import TEST_DID0
from ...base import ResolverError

# pylint: disable=W0621

@pytest.fixture
def resolver():
    """Resolver fixture."""
    yield IndyDIDResolver()

@pytest.fixture
def ledger():
    """Ledger fixture."""
    ledger = async_mock.MagicMock()
    ledger.get_endpoint_for_did = async_mock.CoroutineMock(return_value="endpoint")
    ledger.get_key_for_did = async_mock.CoroutineMock(return_value="key")
    yield ledger

@pytest.fixture
def session(ledger):
    """Session fixture."""
    session = InMemoryProfile.test_session()
    session.context.injector.bind_instance(IndySdkLedger, ledger)
    yield session

def test_supported_methods(resolver: IndyDIDResolver):
    """Test the supported_methods."""
    assert resolver.supported_methods == ["sov"]
    assert resolver.supports("sov")

@pytest.mark.asyncio
async def test_resolve(resolver: IndyDIDResolver, session: ProfileSession):
    """Test resolve mtehod."""
    assert await resolver.resolve(session, TEST_DID0)

@pytest.mark.asyncio
async def test_resolve_x(resolver: IndyDIDResolver, session: ProfileSession):
    """Test resolve mtehod with no ledger."""
    session.context.injector.clear_binding(IndySdkLedger)
    with pytest.raises(ResolverError):
        await resolver.resolve(session, TEST_DID0)
