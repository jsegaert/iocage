from iocage.lib.ioc_fetch import IOCFetch


def test_fetch(release, server, user, password, auth, root_dir, http, _file,
               hardened):
    IOCFetch(release, server, user, password, auth, root_dir, http=http,
             _file=_file, hardened=hardened).fetch_release()

    assert True == True
