import pytest
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


def check_expected(expected, actual, percent_threshold):
    return abs(actual - expected) / expected * 100 < percent_threshold


def swap_single_check(ib_token_in, ib_token_out, amount_in, account):
    # set input and output ibtoken contracts
    token_in_safebox = Contract.from_abi("SafeBox", ib_token_in, SAFEBOX_ABI)
    token_out_safebox = Contract.from_abi("SafeBox", ib_token_out, SAFEBOX_ABI)
    # deploy contract
    homora_earn_swap = HomoraIBSwap.deploy(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1", {"from": account}
    )
    # approve ibtokens
    homora_earn_swap.addIBTokens([IBUSDT_ADDRESS, IBUSDC_ADDRESS, IBDAI_ADDRESS], {"from": account})
    # estimate expected output token amount from swap
    underlying_amount_in = homora_earn_swap.ibToToken(ib_token_in, amount_in)
    estimate_amount_out = homora_earn_swap.getEstimatedAmountsOut(ib_token_in, ib_token_out, underlying_amount_in)[1]
    # perform the swap
    token_in_safebox.approve(homora_earn_swap.address, 1e36, {"from": account})
    output = homora_earn_swap.swap(
        ib_token_in,
        ib_token_out,
        amount_in,
        homora_earn_swap.tokenToIB(ib_token_out, int(estimate_amount_out * 0.9)),
        deadline,
        {"from": account},
    )
    return (homora_earn_swap, token_in_safebox, token_out_safebox, estimate_amount_out, output.return_value)


def swap_double_check(ib_token_in, ib_token_out, amount_in, account):
    # set input and output ibtoken contracts
    token_in_safebox = Contract.from_abi("SafeBox", ib_token_in, SAFEBOX_ABI)
    token_out_safebox = Contract.from_abi("SafeBox", ib_token_out, SAFEBOX_ABI)
    # deploy contract
    homora_earn_swap = HomoraIBSwap.deploy(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D", "0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1", {"from": account}
    )
    # approve ibtokens
    homora_earn_swap.addIBTokens([IBUSDT_ADDRESS, IBUSDC_ADDRESS, IBDAI_ADDRESS], {"from": account})
    # estimate expected output token amount from swap
    underlying_amount_in = homora_earn_swap.ibToToken(ib_token_in, amount_in)
    estimate_amount_out = homora_earn_swap.getEstimatedAmountsOut(ib_token_in, ib_token_out, underlying_amount_in)[2]
    # perform the swap
    token_in_safebox.approve(homora_earn_swap.address, 1e36, {"from": account})
    output = homora_earn_swap.swap(
        ib_token_in,
        ib_token_out,
        amount_in,
        homora_earn_swap.tokenToIB(ib_token_out, int(estimate_amount_out * 0.9)),
        deadline,
        {"from": account},
    )
    return (homora_earn_swap, token_in_safebox, token_out_safebox, estimate_amount_out, output.return_value)


# swap from ibethv2 vto ibusdtv2
def test_general_eth_usdt(account):
    # swap parameters
    amount_in = 992637183
    token_in = IBETH_ADDRESS
    token_out = IBUSDC_ADDRESS
    # deploy contract and approve input token
    (homora_earn_swap, _, _, estimate_amount_out, actual_amount_out) = swap_single_check(
        token_in, token_out, amount_in, account
    )
    assert check_expected(actual_amount_out, homora_earn_swap.tokenToIB(token_out, estimate_amount_out), 0.5,)


# swap from ibusdtv2 to ibethv2
def test_general_usdt_eth(account):
    # swap parameters
    amount_in = 8e12
    token_in = IBUSDT_ADDRESS
    token_out = IBETH_ADDRESS
    # deploy contract and approve input token
    (homora_earn_swap, _, _, estimate_amount_out, actual_amount_out) = swap_single_check(
        token_in, token_out, amount_in, account
    )
    assert check_expected(actual_amount_out, homora_earn_swap.tokenToIB(token_out, estimate_amount_out), 0.5,)


# swap from ibusdtv2 to ibusdcv2
def test_general_usdt_usdc(account):
    # swap parameters
    amount_in = 8e12
    token_in = IBUSDT_ADDRESS
    token_out = IBUSDC_ADDRESS
    # deploy contract and approve input token
    (homora_earn_swap, _, _, estimate_amount_out, actual_amount_out) = swap_double_check(
        token_in, token_out, amount_in, account
    )
    assert check_expected(actual_amount_out, homora_earn_swap.tokenToIB(token_out, estimate_amount_out), 0.5,)


# swap ibusdtv2 to ibdaiv2
def test_general_usdt_dai(account):
    # swap parameters
    amount_in = 8e12
    token_in = IBUSDT_ADDRESS
    token_out = IBDAI_ADDRESS
    # deploy contract and approve input token
    (homora_earn_swap, _, _, estimate_amount_out, actual_amount_out) = swap_double_check(
        token_in, token_out, amount_in, account
    )
    assert check_expected(actual_amount_out, homora_earn_swap.tokenToIB(token_out, estimate_amount_out), 0.5,)

