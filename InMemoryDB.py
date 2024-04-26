class InMemoryDB:
    def __init__(self):
        self.main_store = {}
        self.transaction_store = {}
        self.in_transaction = False

    def get(self, key):
        if key in self.transaction_store and self.in_transaction:
            return self.transaction_store[key]
        return self.main_store.get(key, None)

    def put(self, key, value):
        if not self.in_transaction:
            raise Exception("No transaction in progress")
        self.transaction_store[key] = value

    def begin_transaction(self):
        if self.in_transaction:
            raise Exception("Transaction already in progress")
        self.in_transaction = True
        self.transaction_store = {}

    def commit(self):
        if not self.in_transaction:
            raise Exception("No transaction in progress")
        self.main_store.update(self.transaction_store)
        self.in_transaction = False
        self.transaction_store = {}

    def rollback(self):
        if not self.in_transaction:
            raise Exception("No transaction in progress")
        self.in_transaction = False
        self.transaction_store = {}


if __name__ == "__main__":
    db = InMemoryDB()
    
    print(db.get("A"))
    try:
        db.put("A", 5)
    except Exception as e:
        print(e)
    
    db.begin_transaction()
    db.put("A", 5)
    print(db.get("A"))
    
    db.put("A", 6)
    db.commit()
    print(db.get("A"))
    
    try:
        db.commit()
    except Exception as e:
        print(e)
    
    try:
        db.rollback()
    except Exception as e:
        print(e)
    
    print(db.get("B"))
    db.begin_transaction()
    db.put("B", 10)
    db.rollback()
    print(db.get("B"))
