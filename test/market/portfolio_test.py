from graffiti.market import Portfolio


def test_portfolio_basic_operations():
    p = Portfolio()

    p.add_security("USD", 100)
    assert p.get("USD") == 100
    assert p["USD"] == 100

    p.add_security("USD", -50)
    assert p.get("USD") == 50
    assert p["USD"] == 50

    p.remove_security("USD")
    assert p.get("USD") == 0
    assert p["USD"] == 0
    assert ("USD" not in p.securities)

    assert p.get("CAD") == 0
    assert p["CAD"] == 0

    p["EUR"] = 200
    assert p.get("EUR") == 200
    assert p["EUR"] == 200
