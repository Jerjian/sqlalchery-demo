# Tutorial: https://www.youtube.com/watch?v=xr7vDSFXjW0&t=227s

from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

engine = create_engine('sqlite:///orm.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    #relationship
    posts = relationship("Post", back_populates="user") 
    
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, Sequence('post_id_seq'), primary_key=True)
    title = Column(String(50))
    content = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    #relationship
    user = relationship("User", back_populates="posts")


Base.metadata.create_all(engine)
user1 = User(name='Alice', email = 'alice@example.com')
user2 = User(name='Bob', email='bob@example.com')
post1 = Post(title="Alice First Post" , content="This is Alice's first post", user=user1)
post2 = Post(title="Alice Second Post" , content="This is Alice's Second post", user=user1)
post3 = Post(title="Bob First Post" , content="This is Bobs first post", user=user2)

session.add_all([user1, user2])
session.add_all([post1, post2, post3])
session.commit()

# Joining tables
posts_with_users = session.query(Post, User).join(User).all()
# for post, user in posts_with_users:
#     print(f"Post Title: {post.title}, User Name: {user.name}")

# Querying posts by user
alice = session.query(User).filter_by(name='Alice').first()
# for post in alice.posts:
#     print(f"Alice's Post Title: {post.title}")  

#advanced query
filtered_posts = session.query(Post).join(User).filter(User.name == 'Alice').all()
for post in filtered_posts:
    print(f"Filtered Post Title: {post.title}, User Name: {post.user.name}")