import yaml
from tests.fixtures import tmp_campaign

from npc.campaign import Campaign

def test_gets_global_type(tmp_campaign):
    chartype = tmp_campaign.get_type("person")

    assert chartype.name == "Person"

def test_gets_local_type(tmp_campaign):
    pet_def = {
        "pet": {
            "name": "Pet",
            "desc": "A domestic animal kept for companionship"
        }
    }
    new_type_file = tmp_campaign.settings_dir.joinpath("types", "pet.yaml")
    new_type_file.parent.mkdir()
    new_type_file.touch()
    with new_type_file.open('w', newline="\n") as f:
        yaml.dump(pet_def, f)

    chartype = tmp_campaign.get_type("pet")

    assert chartype.name == "Pet"
