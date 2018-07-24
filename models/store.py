from db import db

class StoreModel(db.Model):
    __tablename__='stores'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name=name
    def json(self):
        # items = list(map(lambda item:item.json(),self.items))
        return {'id':self.id,
                'name':self.name, 
                'items':[item.json() for item in self.items.all()]
                }

    @classmethod
    def find_by_name(cls, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # res=cursor.execute(query, (name,))
        # row = res.fetchone()
        # connection.close()
        # if row:
        #     return cls(*row)

        #SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        # connection=sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES(?,?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
