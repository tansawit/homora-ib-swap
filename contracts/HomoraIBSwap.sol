// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.7.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/SafeERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "./Governable.sol";
import "../interfaces/IWETH.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/ISafeBox.sol";
import "../interfaces/ISafeBoxETH.sol";
import "../interfaces/ICErc20.sol";
import "../interfaces/ICyToken.sol";

/// @title Homora IBToken Swap
/// @author Sawit Trisirisatayawong (@tansawit)
contract HomoraIBSwap is Governable {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    mapping(address => bool) public isIBToken;

    address public immutable IBETHV2;

    IUniswapV2Router02 public immutable router;

    address public immutable WETH;

    constructor(address _routerAddress, address _ibETHAddress) public {
        __Governable__init();
        router = IUniswapV2Router02(_routerAddress);
        IBETHV2 = _ibETHAddress;
        isIBToken[_ibETHAddress] = true;
        WETH = IUniswapV2Router02(_routerAddress).WETH();

        IWETH(IUniswapV2Router02(_routerAddress).WETH()).approve(
            _routerAddress,
            uint256(-1)
        );
        IWETH(IUniswapV2Router02(_routerAddress).WETH()).approve(
            _ibETHAddress,
            uint256(-1)
        );
    }

    /// @notice add a list of token addresses as supported ibToken
    /// @param tokens list of symbols to support
    function addIBTokens(address[] calldata tokens) external onlyGov {
        for (uint256 idx = 0; idx < tokens.length; idx++) {
            require(
                !isIBToken[tokens[idx]] && tokens[idx] != IBETHV2,
                "token-is-ibeth-or-already-supported"
            );
            isIBToken[tokens[idx]] = true;

            SafeBox safebox = SafeBox(tokens[idx]);
            address uToken = safebox.uToken();
            IERC20(uToken).safeApprove(address(router), uint256(-1));
            IERC20(uToken).safeApprove(address(safebox), uint256(-1));
        }
    }

    function getPath(address tokenIn, address tokenOut)
        internal
        view
        returns (address[] memory path)
    {
        address underlyingTokenIn;
        address underlyingTokenOut;

        underlyingTokenIn = tokenIn == IBETHV2
            ? WETH
            : SafeBox(tokenIn).uToken();

        underlyingTokenOut = tokenOut == IBETHV2
            ? WETH
            : SafeBox(tokenOut).uToken();

        if (underlyingTokenIn == WETH || underlyingTokenOut == WETH) {
            path = new address[](2);
            if (underlyingTokenIn == WETH) {
                path[0] = WETH;
                path[1] = underlyingTokenOut;
            } else {
                path[0] = underlyingTokenIn;
                path[1] = WETH;
            }
        } else {
            path = new address[](3);
            path[0] = underlyingTokenIn;
            path[1] = WETH;
            path[2] = underlyingTokenOut;
        }
    }

    /// @notice get the estimated outpout amount of each consecutive
    /// swap along a path
    /// @param tokenIn the address of the input token
    /// @param tokenOut the address of the output token
    /// @param amountIn the inputted amount of tokenIn
    function getEstimatedAmountsOut(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) public view returns (uint256[] memory) {
        require(tokenIn != tokenOut, "token-in-out-identical");
        return router.getAmountsOut(amountIn, getPath(tokenIn, tokenOut));
    }

    /// @notice convert an amount of ibToken to that of the underlying token
    /// @param ibToken the ibToken to get the underlying token amount of
    /// @param ibTokenAmount the amount of ibToken to use for conversion
    function ibToToken(address ibToken, uint256 ibTokenAmount)
        external
        view
        returns (uint256)
    {
        CYToken cyToken = CYToken(SafeBox(ibToken).cToken());
        return ibTokenAmount.mul(cyToken.exchangeRateStored()).div(1e18);
    }

    /// @notice convert an amount of token to that of the associated ibToken
    /// @param ibToken the ibToken to get the token amount of
    /// @param tokenAmount the amount of token to use for conversion
    function tokenToIB(address ibToken, uint256 tokenAmount)
        external
        view
        returns (uint256)
    {
        CYToken cyToken = CYToken(SafeBox(ibToken).cToken());
        return tokenAmount.mul(1e18).div(cyToken.exchangeRateStored());
    }

    /// @notice swap an ibToken to another ibToken
    /// @param tokenIn the input ibToken
    /// @param tokenOut the desired output ibToken
    /// @param amountIn the amount of tokenIn to swap
    /// @param amountOutMin minimum amount of output tokens that must be received
    /// for the transaction not to revert
    /// @param deadline timestamp after which the transaction will revert
    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn,
        uint256 amountOutMin,
        uint256 deadline
    ) external returns (uint256) {
        require(tokenIn != tokenOut, "token-in-out-identical");
        require(isIBToken[tokenIn], "token-in-not-supported");
        require(isIBToken[tokenOut], "token-out-not-supported");

        uint256 underlyingBalance;
        address[] memory path = getPath(tokenIn, tokenOut);
        uint256 outputAmount;

        SafeBox(tokenIn).transferFrom(msg.sender, address(this), amountIn);
        SafeBox(tokenIn).withdraw(amountIn);

        if (tokenIn == IBETHV2) {
            IWETH(WETH).deposit{value: address(this).balance}();
            underlyingBalance = IWETH(WETH).balanceOf(address(this));
        } else {
            IERC20 underlying = IERC20(SafeBox(tokenIn).uToken());
            underlyingBalance = underlying.balanceOf(address(this));
        }

        router.swapExactTokensForTokens(
            underlyingBalance,
            0,
            path,
            address(this),
            deadline
        );

        if (tokenOut == IBETHV2) {
            IWETH(WETH).withdraw(IWETH(WETH).balanceOf(address(this)));
            SafeBoxETH safeboxOut = SafeBoxETH(tokenOut);
            safeboxOut.deposit{value: address(this).balance}();
        } else {
            SafeBox safeboxOut = SafeBox(tokenOut);
            safeboxOut.deposit(
                IERC20(safeboxOut.uToken()).balanceOf(address(this))
            );
        }
        outputAmount = SafeBox(tokenOut).balanceOf(address(this));
        SafeBox(tokenOut).transfer(msg.sender, outputAmount);

        require(outputAmount >= amountOutMin, "insufficient-output-amount");
        return outputAmount;
    }

    receive() external payable {
        require(
            msg.sender == WETH ||
                msg.sender == IBETHV2 ||
                msg.sender == address(router),
            "unexpected-eth-sender"
        );
    }
}
