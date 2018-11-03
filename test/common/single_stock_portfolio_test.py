from dsi.common.single_stock_portoflio import SingleStockPortfolio


def test_single_stock_portfolio_basic_buy_sell():
    p = SingleStockPortfolio(initial_currency=1000.0)
    p.buy(10.0, 10.0)
    assert p.get_currency() == 1000 - 10*10
    assert p.get_stock() == 10

    p.sell(5, 5)
    assert p.get_currency() == 900 + 25
    assert p.get_stock() == 5
