from webapp import db # The SQLAlchemy object created in __init__.py

class User(db.Model):
    
    # Create database 'fields' using the db.Column class, with the datatype and additional specifications as arguments
    
    id = db.Column(db.Integer, primary_key = True) # Each user in the database will be automatically assigned a unique id value
    username = db.Column(db.String(64), index = True, unique = True) # Set the maximum size as 64 characters, for optimal space usage
    email = db.Column(db.String(120), index=True, unique=True) 
    password_hash = db.Column(db.String(128)) # Writing password hashes instead of passwords directly, to improve security
    
    # Method to tell Python how to print objects of this class--useful for debugging
    def __repr__(self):
        return '<User {}>'.format(self.username)

