import pytest
import brownie
from brownie import accounts, Contract, HomoraIBSwap

SAFEBOX_ABI = [
    {
        "inputs": [
            {"internalType": "contract ICErc20", "name": "_cToken", "type": "address"},
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_symbol", "type": "string"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "spender", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "user", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "Claim",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "from", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "to", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"},
        ],
        "name": "Transfer",
        "type": "event",
    },
    {"inputs": [], "name": "acceptGovernor", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "adminClaim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "cToken",
        "outputs": [{"internalType": "contract ICErc20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "totalReward", "type": "uint256"},
            {"internalType": "bytes32[]", "name": "proof", "type": "bytes32[]"},
        ],
        "name": "claim",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "claimAmount", "type": "uint256"},
            {"internalType": "bytes32[]", "name": "proof", "type": "bytes32[]"},
            {"internalType": "uint256", "name": "withdrawAmount", "type": "uint256"},
        ],
        "name": "claimAndWithdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "claimed",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
        ],
        "name": "decreaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "governor",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
        ],
        "name": "increaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "pendingGovernor",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "relayer",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "root",
        "outputs": [{"internalType": "bytes32", "name": "", "type": "bytes32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_pendingGovernor", "type": "address"}],
        "name": "setPendingGovernor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_relayer", "type": "address"}],
        "name": "setRelayer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "sender", "type": "address"},
            {"internalType": "address", "name": "recipient", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "uToken",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "bytes32", "name": "_root", "type": "bytes32"}],
        "name": "updateRoot",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]

IBETH_ADDRESS = "0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1"

USDT_ADDRESS = "0xdac17f958d2ee523a2206206994597c13d831ec7"
IBUSDT_ADDRESS = "0x020EDC614187F9937A1EFEEE007656C6356FB13A"

USDC_ADDRESS = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
IBUSDC_ADDRESS = "0x08bd64BFC832F1C2B3e07e634934453bA7Fa2db2"

DAI_ADDRESS = "0x6b175474e89094c44da98b954eedeac495271d0f"
IBDAI_ADDRESS = "0xee8389d235E092b2945fE363e97CDBeD121A0439"

WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

utoken_to_ibtoken = dict(
    {
        IBETH_ADDRESS: IBETH_ADDRESS,
        USDT_ADDRESS: IBUSDT_ADDRESS,
        USDC_ADDRESS: IBUSDC_ADDRESS,
        DAI_ADDRESS: IBDAI_ADDRESS,
    }
)

ibtoken_to_utoken = dict(
    {
        IBETH_ADDRESS: IBETH_ADDRESS,
        IBUSDT_ADDRESS: USDT_ADDRESS,
        IBUSDC_ADDRESS: USDC_ADDRESS,
        IBDAI_ADDRESS: DAI_ADDRESS,
    }
)

deadline = 1e21


@pytest.fixture
def account():
    return accounts.at("0xcdc2F106E9694B16FFdBFCE2a2612076Ce44b4FE", force=True)


def test_revert_send_ether(account):
    homora_earn_swap = HomoraIBSwap.deploy(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1", {"from": account}
    )
    with brownie.reverts("unexpected-eth-sender"):
        account.transfer(homora_earn_swap, "0.5 ether")


def test_revert_add_ib_tokens(account):
    ens = accounts.at("0x37fabbfaf80501c68ee77625d620d6501b35417e", force=True)
    homora_earn_swap = HomoraIBSwap.deploy(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1", {"from": account}
    )
    with brownie.reverts("not the governor"):
        tx = homora_earn_swap.addIBTokens([IBUSDT_ADDRESS, IBUSDC_ADDRESS, IBDAI_ADDRESS], {"from": ens})

