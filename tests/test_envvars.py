
def test_dummy(testdir):
    testdir.makepyfile("""
            def test_dummy():
                assert 1 == 1
        """)

    result = testdir.runpytest('--envvars-validate')

    assert result.ret == 0
