from . import db
import bcrypt
from datetime import datetime


# defines model for user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    birthdate = db.Column(db.String(10))
    blood_type = db.Column(db.String(3))
    phone = db.Column(db.String(11))
    sex = db.Column(db.Boolean)
    qty_donations = db.Column(db.Integer)
    date_last_donation = db.Column(db.String(10))
    state = db.Column(db.String(30))
    city = db.Column(db.String(60))
    donation_order = db.relationship("Donation_order", backref="user")
    posts = db.relationship("Posts", backref="user")
    comments = db.relationship("Comments", backref="user")
    password_reset_token = db.Column(db.String(6))
    photo = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def to_dict(self, private=False):
        
        if private:
            return {
                'id': str(self.id),
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'qty_donations': (self.qty_donations),
                'date_last_donation': self.date_last_donation,
                'state': self.state,
                'city': self.city,
                'donations_orders': f'{self.get_donations()}',
                'posts': f'{self.get_posts()}',
                'photo': self.photo
            }
            
        return {
            'id': str(self.id),
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthdate': self.birthdate,
            'blood_type': self.blood_type,
            'phone': self.phone,
            'sex': bool(self.sex),
            'qty_donations': (self.qty_donations),
            'date_last_donation': self.date_last_donation,
            'state': self.state,
            'city': self.city,
            'donations_orders': f'{self.get_donations()}',
            'posts': f'{self.get_posts()}',
            'comments': f'{self.get_comments()}',
            'password_reset_token': self.password_reset_token,
            'photo': self.photo
        }

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')
        
    def set_token(self, token):
        hashed_token = bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt())
        self.password_reset_token = hashed_token.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
   
    def check_token(self, token):
        return bcrypt.checkpw(token.encode('utf-8'), self.password_reset_token.encode('utf-8'))
    
    def get_donations(self):
         orders_list = []
         for i in range(len(self.donation_order)):
              orders_list.append(self.donation_order[i].id)
         return orders_list
    
    def get_posts(self):
         posts_list = []
         for i in range(len(self.posts)):
              posts_list.append(self.posts[i].id)
         return posts_list
    
    def get_comments(self):
         comments_list = []
         for i in range(len(self.comments)):
              comments_list.append(self.comments[i].id)
         return comments_list

class Hospitals(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     hospital_name = db.Column(db.String(80), unique=True, nullable=False)
     city_name = db.Column(db.String(80), nullable=False)
     state = db.Column(db.Integer, nullable=False)
     donations_orders = db.Column(db.Integer)
     donations_orders_done = db.Column(db.Integer)
     donations_orders_cancelled = db.Column(db.Integer)
     donation_order = db.relationship("Donation_order", backref='hospitals')
     latitude = db.Column(db.Float, nullable=True)
     longitude = db.Column(db.Float, nullable=True)

     def __repr__(self):
        return '<Hospitals %r>' % self.hospital_name
     
     def to_dict(self):
            return {
                'id': str(self.id),
                'hospital_name': self.hospital_name,
                'city_name': self.city_name,
                'state': self.state,
                'donations_orders': self.donations_orders,
                'donations_orders_done': self.donations_orders_done,
                'donations_orders_cancelled': self.donations_orders_cancelled,
                'latitude': self.latitude,
                'longitude': self.longitude
            }

class Donation_order(db.Model):  # TODO Update or handle integer for blood type
    
     id = db.Column(db.Integer, primary_key=True)
     patient_name = db.Column(db.String(80), nullable=False)
     blood_type = db.Column(db.String(3), nullable=False)
     description = db.Column(db.String(500))
     qty_bags = db.Column(db.Integer)
     date_donation_order = db.Column(db.DateTime, default=datetime.utcnow)
     city_name = db.Column(db.String(80))
     state = db.Column(db.Integer)
     hospital = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
     requester = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
     status = db.Column(db.String(40), default="open")

        # TODO Maybe do a set adress function to get the same as the hospital

     def __repr__(self):
        return '<Donation_order %r>' % self.patient_name

     def to_dict(self):
            return {
                'id': str(self.id),
                'patient_name': self.patient_name,
                'blood_type': self.blood_type,
                'description': self.description,
                'qty_bags': self.qty_bags,
                'date_donation_order': self. date_donation_order,
                'hospital': self.hospitals.to_dict(),
                'requester': self.user.to_dict(),
                'status': self.status,
                'city_name': self.city_name
            }

     
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='post')
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f'<Post "{self.title}">'
    
    def to_dict(self):   # TODO Find a way to show all posts in the user route
         return{
              'id': self.id,
              'title': self.title,
              'content': self.content,
              'created at': self.created_at,
              'comments': f'{self.get_comments()}',
              'user': self.user.to_dict(private=True)
         }

    def get_comments(self):
         
         comments_list = []
         for i in range(len(self.comments)):
              comments_list.append(self.comments[i].id)
         return comments_list


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'
    
    def to_dict(self):
         return {
              'id': self.id,
              'content': self.content,
              'post_id': self.post_id,
              'created_at': self.created_at,
              'user_id': self.user_id
         }