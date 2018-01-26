import pymongo
from bson.objectid import ObjectId

DATABASE = "bp"


class DBHelper:

    def __init__(self):
        # Python object that will let us run the CRUD operations on our
        # database.
        client = pymongo.MongoClient()
        self.db = client[DATABASE]

    # Users.
    def get_user(self, email):
        return self.db.users.find_one({"email": email})

    def add_user(self, email, salt, hashed):
        self.db.users.insert({"email": email, "salt": salt, "hashed": hashed})

    # Tables.
    def add_table(self, number, owner):
        new_id = self.db.tables.insert({"number": number, "owner": owner})
        return new_id

    def update_table(self, _id, url):
        self.db.tables.update({"_id": _id}, {"$set": {"url": url}})

    def get_tables(self, owner_id):
        return list(self.db.tables.find({"owner": owner_id}))

    def get_table(self, table_id):
        return self.db.tables.find_one({"_id": ObjectId(table_id)})

    def delete_table(self, table_id):
        self.db.tables.remove({"_id": ObjectId(table_id)})

    # Requests.
    def add_request(self, table_id, time):
        table = self.get_table(table_id)
        try:
            self.db.requests.insert({"owner": table['owner'],
                "table_number": table['number'],
                "table_id": table_id,
                "time": time})
            return True
        except pymongo.errors.DuplicateKeyError:
            return False

    def get_requests(self, owner_id):
        return list(self.db.requests.find({"owner": owner_id}))

    def delete_request(self, request_id):
        self.db.requests.remove({"_id": ObjectId(request_id)})

    # Measurements.
    def add_measurement(self, owner_id, date_time, sys_mmhg, dia_mmhg, pul):
        new_id = self.db.measurements.insert({"owner_id": owner_id,
                                              "date_time": date_time,
                                              "sys_mmhg": sys_mmhg,
                                              "dia_mmhg": dia_mmhg,
                                              "pul": pul})
        return new_id

    def get_measurements(self, owner_id):
        return list(self.db.measurements.find({"owner_id": owner_id}))

    def get_measurement(self, measurement_id):
        return self.db.measurements.find_one({"_id": ObjectId(measurement_id)})

    def delete_measurement(self, measurement_id):
        self.db.measurements.remove({"_id": ObjectId(measurement_id)})
