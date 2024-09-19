from app import db, Club, User, Tag
db.drop_all()
db.create_all()
#newUser = User(name="thomas") 
'''
tag1 = Tag(tagname="CS")
tag2 = Tag(tagname="Writing")
tag3 = Tag(tagname="Film")
tag4 = Tag(tagname="Art")
tag5 = Tag(tagname="Music")
tag6 = Tag(tagname="Visual Arts")
myClub = Club.query.get(1)
myClub.tags.append(tag1)
myClub.tags.append(tag2)
myClub.tags.append(tag3)
myClub.tags.append(tag4)
db.session.add_all([tag1,tag2,tag3,tag4,tag5,tag6,myClub])
db.session.commit()
'''


