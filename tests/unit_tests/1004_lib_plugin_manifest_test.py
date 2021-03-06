import pytest

from iocage_lib.ioc_common import validate_plugin_manifest

VALID_MANIFEST = {
    "name": "test_plugin",
    "release": "12.2-RELEASE",
    "pkgs": [],
    "packagesite": "http://pkg.FreeBSD.org/${ABI}/latest",
    "fingerprints": {
        "iocage-plugins": [
            {
                "function": "sha256",
                "fingerprint": "b0170035af3acc5f3f3ae1859dc717101b4e6c1d0a794ad554928ca0cbb2f438"
            }
        ]
    },
    "artifact": "TEST_ARTIFACT",
}


def test_validate_plugin_manifest():
    validate_plugin_manifest(VALID_MANIFEST, None, None)


@pytest.mark.parametrize(
    "missing_field",
    ["name", "release", "pkgs", "packagesite", "fingerprints", "artifact"]
)
def test_missing_required_fields(missing_field):
    manifest = VALID_MANIFEST.copy()
    del manifest[missing_field]

    exp_msg = f"'{missing_field}' is a required property"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_missing_multiple_required_fields():
    manifest = VALID_MANIFEST.copy()
    del manifest["name"]
    del manifest["packagesite"]

    exp_msg = "'name' is a required property\n"
    exp_msg += "'packagesite' is a required property"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_devfs_ruleset_not_dict():
    manifest = VALID_MANIFEST.copy()
    manifest["devfs_ruleset"] = "INVALID_TYPE"

    exp_msg = "'INVALID_TYPE' is not of type 'object'"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_devfs_ruleset_missing_paths():
    manifest = VALID_MANIFEST.copy()
    manifest["devfs_ruleset"] = {}

    exp_msg = "'paths' is a required property"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_devfs_ruleset_invalid_paths_type():
    manifest = VALID_MANIFEST.copy()
    manifest["devfs_ruleset"] = {
        "paths": "INVALID_TYPE",
    }

    exp_msg = "'INVALID_TYPE' is not of type 'object'"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_devfs_ruleset_invalid_includes_type():
    manifest = VALID_MANIFEST.copy()
    manifest["devfs_ruleset"] = {
        "paths": {},
        "includes": "INVALID_TYPE"
    }

    exp_msg = "'INVALID_TYPE' is not of type 'array'"
    with pytest.raises(RuntimeError, match=exp_msg):
        validate_plugin_manifest(manifest, None, None)


def test_valid_devfs_ruleset():
    manifest = VALID_MANIFEST.copy()
    manifest["devfs_ruleset"] = {
        "paths": {},
        "includes": []
    }

    validate_plugin_manifest(manifest, None, None)
