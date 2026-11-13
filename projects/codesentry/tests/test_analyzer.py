from codesentry.analyzer import Analyzer

def test_risky_calls_and_broad_except():
    source="def f(x):\n    try:\n        eval(x)\n    except Exception:\n        pass\n"
    rules={x["rule"] for x in Analyzer(source,"sample.py").report()["findings"]}
    assert {"DYNAMIC_EXECUTION","BROAD_EXCEPTION"}<=rules

def test_complexity():
    r=Analyzer("def f(x):\n    if x:\n        return 1\n    return 0\n").report()
    assert r["functions"][0]["complexity"]==2

def test_syntax_error():
    assert Analyzer("def broken(:\n pass").report()["findings"][0]["rule"]=="SYNTAX_ERROR"
