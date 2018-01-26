# We'll create a MockDBHelper class again and also create a con guration
# le to indicate that this should be used locally when we test our
# application and don't have access to the database. It needs to have a
# function that takes a username and password and checks whether these
# exist in the database and are associated with each other.

import datetime

# This dect acts as the database storage.

MOCK_USERS = [{"email": "test@example.com",
               "salt": "8Fb23mMNHD5Zb8pr2qWA3PE9bH0=",
               "hashed": "1736f83698df3f8153c1fbd6ce2840f8aace4f200771a46672635374073cc876cf0aa6a31f780e576578f791b5555b50df46303f0c3a7f2d21f91aa1429ac22e"}]

MOCK_TABLES = [{"_id": "1",
                "number": "1",
                "owner": "test@example.com",
                "url": "mockurl"}]

MOCK_REQUESTS = [{"_id": "1",
                  "table_number": "1",
                  "table_id": "1",
                  "time": datetime.datetime.now()}]

MOCK_MEASUREMENTS = [{"_id": "1",
                      "date_time": datetime.datetime.now(),
                      "sys_mmhg": "120",
                      "dia_mmhg": "80",
                      "pul": "70"}]


class MockDBHelper:

    def get_user(self, email):
        user = [x for x in MOCK_USERS if x.get("email") == email]
        if user:
            return user[0]
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({"email": email, "salt": salt, "hashed": hashed})

    # Measurements:
    # To Do: add owner to measurement
    def add_measurement(self, owner_id, date_time, sys, dia, pul):
        MOCK_MEASUREMENTS.append({"_id": "0",
                                  "owner_id": owner_id,
                                  "date_time": date_time,
                                  "sys_mmhg": sys,
                                  "dia_mmhg": dia,
                                  "pul": pul})
        return True

    def delete_measurement(self, measurement_id):
        for i, mea in enumerate(MOCK_MEASUREMENTS):
            if mea.get("_id") == measurement_id:
                del MOCK_MEASUREMENTS[i]
                break

    def get_measurements(self, owner_id):
        return MOCK_MEASUREMENTS

    def get_measurement(self, measurement_id):
        for mea in MOCK_MEASUREMENTS:
            if mea.get("_id") == measurement_id:
                return mea
