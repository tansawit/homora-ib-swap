pragma solidity ^0.7.0;

import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC20/SafeERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/math/SafeMath.sol";
import "../interfaces/IUniswapV2Router02.sol";
import "../interfaces/ISafeBox.sol";
import "../interfaces/ISafeBoxETH.sol";
import "../interfaces/ICErc20.sol";
import "../interfaces/ICyToken.sol";

contract HomoraIBSwap {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    address private constant IBETHV2 =
        0xeEa3311250FE4c3268F8E684f7C87A82fF183Ec1;
    address private constant IBUSDTV2 =
        0x020eDC614187F9937A1EfEeE007656C6356Fb13A;
    address private constant IBUSDCV2 =
        0x08bd64BFC832F1C2B3e07e634934453bA7Fa2db2;
    address private constant IBDAIV2 =
        0xee8389d235E092b2945fE363e97CDBeD121A0439;

    address internal constant UNISWAP_ROUTER_ADDRESS =
        0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    IUniswapV2Router02 public uniswapRouter;

    constructor() {
        uniswapRouter = IUniswapV2Router02(UNISWAP_ROUTER_ADDRESS);
    }

    function supported(address token) public returns (bool) {
        if (
            token == IBETHV2 ||
            token == IBUSDTV2 ||
            token == IBUSDCV2 ||
            token == IBDAIV2
        ) {
            return true;
        }
        return false;
    }

    function path(uint256 order, address token)
        internal
        view
        returns (address[] memory)
    {
        address[] memory path = new address[](2);
        if (order == 0) {
            path[0] = uniswapRouter.WETH();
            path[1] = token;
        } else {
            path[0] = token;
            path[1] = uniswapRouter.WETH();
        }
        return path;
    }

    function getEstimateAmountOut(
        uint256 order,
        address token,
        uint256 amountIn
    ) public view returns (uint256[] memory) {
        return uniswapRouter.getAmountsOut(amountIn, path(order, token));
    }

    function ibToToken(address ibToken, uint256 ibTokenAmount)
        external
        view
        returns (uint256)
    {
        CYToken cyToken = CYToken(SafeBox(ibToken).cToken());
        uint256 tokenAmount =
            ibTokenAmount.mul(cyToken.exchangeRateStored()).div(1e18);
        return tokenAmount;
    }

    function tokenToIB(address ibToken, uint256 tokenAmount)
        external
        view
        returns (uint256)
    {
        CYToken cyToken = CYToken(SafeBox(ibToken).cToken());
        uint256 ibTokenAmount =
            tokenAmount.mul(1e18).div(cyToken.exchangeRateStored());
        return ibTokenAmount;
    }

    function swap(
        address tokenIn,
        address tokenOut,
        uint256 amountIn
    ) external returns (uint256) {
        require(supported(tokenIn), "token-in-not-supported");
        require(supported(tokenOut), "token-out-not-supported");

        SafeBox safeboxIn = SafeBox(tokenIn);

        safeboxIn.transferFrom(msg.sender, address(this), amountIn);
        safeboxIn.withdraw(amountIn);

        uint256 deadline = block.timestamp.add(120);

        if (tokenIn != IBETHV2) {
            IERC20 underlying = IERC20(safeboxIn.uToken());
            uint256 underlyingBalance = underlying.balanceOf(address(this));

            uint256 amountOutMin =
                getEstimateAmountOut(1, safeboxIn.uToken(), underlyingBalance)[
                    1
                ]
                    .mul(9)
                    .div(10);
            address[] memory path = path(1, safeboxIn.uToken());

            underlying.safeApprove(UNISWAP_ROUTER_ADDRESS, underlyingBalance);

            uniswapRouter.swapExactTokensForETH(
                underlyingBalance,
                amountOutMin,
                path,
                address(this),
                deadline
            );
        }
        uint256 outputAmount;
        if (tokenOut == IBETHV2) {
            SafeBoxETH safeboxOut = SafeBoxETH(tokenOut);
            safeboxOut.deposit{value: address(this).balance}();
            outputAmount = safeboxOut.balanceOf(address(this));
            safeboxOut.transfer(
                msg.sender,
                safeboxOut.balanceOf(address(this))
            );
        } else {
            SafeBox safeboxOut = SafeBox(tokenOut);
            IERC20 underlying = IERC20(safeboxOut.uToken());
            uint256 underlyingBalance = underlying.balanceOf(address(this));

            uint256 amountOutMin =
                getEstimateAmountOut(
                    0,
                    safeboxOut.uToken(),
                    address(this).balance
                )[1]
                    .mul(9)
                    .div(10);
            address[] memory path = path(0, safeboxOut.uToken());

            uniswapRouter.swapExactETHForTokens{value: address(this).balance}(
                amountOutMin,
                path,
                address(this),
                deadline
            );

            IERC20(safeboxOut.uToken()).approve(
                address(safeboxOut),
                IERC20(safeboxOut.uToken()).balanceOf(address(this))
            );
            safeboxOut.deposit(
                IERC20(safeboxOut.uToken()).balanceOf(address(this))
            );
            outputAmount = safeboxOut.balanceOf(address(this));
            safeboxOut.transfer(msg.sender, outputAmount);
        }
        return outputAmount;
    }

    receive() external payable {}
}
