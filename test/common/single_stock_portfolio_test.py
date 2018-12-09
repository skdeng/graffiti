from dsi.common.single_asset_portoflio import SingleAssetPortfolio


def test_single_asset_portfolio_basic_buy_sell():
    p = SingleAssetPortfolio(initial_currency=1000.0)
    p.buy(10.0, 10.0)
    assert p.get_currency() == 1000 - 10*10
    assert p.get_asset() == 10

    p.sell(5, 5)
    assert p.get_currency() == 900 + 25
    assert p.get_asset() == 5


def test_single_asset_portfolio_apply_trade_actions():
    pass
