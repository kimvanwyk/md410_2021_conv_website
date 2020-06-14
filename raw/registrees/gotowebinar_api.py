""" Functions to retrieve registree data for the 2020
virtual MD410 Virtual Convention hosted on GoToWebinar
"""

import json
import os.path

import attr
import dateparser
import requests

REFRESH_TOKEN = "v4e5j5s-6lU88Fq9gQ5PWLVZYc3kMH_op_HPL-P58ACTPTUc_gq-om1PLYaV5B30w0b6rPwR50JU1c2-_oniI0BpGjfCFHKh1ZHE.HJWEV6cv_HunVb4vZVdwLcct_-ibP_qdd0mxfqMaYdDuQV9wC773P1g-EpJad_9ETPZimXKmO2m6CsoivM9DKHCrXh1SjiXWUftxJmkddysrJbIvaMdO35uhyTQWW2M92jpdg0bv4S4dswcfTaRwPMnqWw-RUyMD6BSpFG29l51JBTLZpbRCT7R0BRCXbgap-jLHYJ6bJbyy2umhytLVE5IKS5FtgesZAp0ucNWmyc8JkYKMEULhgyAnQsG3jXI2ZlbVNN1unesyIyUtSW_o_F21VxtV23qaydKlovaLHG_M0wIQhiKwZtQtdzQ8vYKBWOcOiL1DumycR3h0ls5ADZg6xB0AYjmxh96Rdb2cfajSWj3ERyPIvcQil47W3jwdPvccufKvavwqtKK0W2PZF3aEJKV6Hn2LDtSz0Z4wyTHiAGB9uKg02L33C3ykchibc9D6m7k9yby2qJMJ06rpC4D7352pGXg25HN8UFy1hJJ0L8GoM3lWfTl-HVyKippvvATQKnJ1LaECemdQ31io3oChJFs5-dGGQwGcuEY44ekI5-A3xA1Sn7aYjq1Mwn5fnpGY4FKG0mKvhlWQXkbMxFtxY8kYRgAcE88P0DVL8vtlqOzwOEv_p9Y-Qal7VAInINWrCb5z_QqdLfGqtoHnXInSvwbF41MWgun3cwD2MlN9j3J3G87cON6CEk2VFzve1uY.fclXWkpmKoAZWj7NTiuBYh5j-veN5Y35dn5fvFVI8-Jke8u0KEssS_JQUrJt6Jkg-joDSfiTrtk8OW8IHcstQfWSIqn_vsSPGSny"
REGISTREES_FN = "registrees.json"


class Api:
    def __init__(self):
        self.get_token()
        try:
            with open(REGISTREES_FN, "r") as fh:
                self.registrees = json.load(fh)
        except Exception:
            self.registrees = {}

        self.get_registrees()

    def get_token(self):
        res = requests.post(
            "https://api.getgo.com/oauth/v2/token",
            params={"refresh_token": REFRESH_TOKEN, "grant_type": "refresh_token"},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic TVZtQ3l5SUNBQzZKdndYdEMyVkxMaldyd0xBMkRmb1k6YVV1R1ZqZXpVemhVQ0Nodg==",
            },
        )
        self.access_token = res.json()["access_token"]

    def get_registrees(self):
        res = requests.get(
            "https://api.getgo.com/G2W/rest/v2/organizers/7707629694462586886/webinars/7600571347013324299/registrants",
            headers={"Authorization": self.access_token},
        )
        l = list(res.json())
        l.sort(key=lambda x: x["registrationDate"])
        n = 0
        for d in l:
            registrant_key = str(d["registrantKey"])
            if registrant_key not in self.registrees:
                self.registrees[registrant_key] = self.get_registree(registrant_key)
                n += 1
        print(f"Added {n} new entries")
        self.write_registrees()

    def get_registree(self, registrant_key):
        res = requests.get(
            f"https://api.getgo.com/G2W/rest/v2/organizers/7707629694462586886/webinars/7600571347013324299/registrants/{registrant_key}",
            headers={"Authorization": self.access_token},
        )
        return {
            "first_name": res.json()["firstName"],
            "last_name": res.json()["lastName"],
            "date": dateparser.parse(res.json()["registrationDate"]).isoformat(),
            "club": res.json()["responses"][0]["answer"],
        }

    def write_registrees(self):
        with open(REGISTREES_FN, "w") as fh:
            json.dump(self.registrees, fh)


if __name__ == "__main__":
    api = Api()
