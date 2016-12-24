import pydelicious as py #import get_popular,get_urlposts,get_userposts

#tag 'programming'
def initUserDict(tag, count=5):
	user_dict = {}
	for p1 in py.get_popular(tag)[0:count]:
		for p2 in py.get_urlposts(p1['href']):
			user = p2['user']
			user_dict[user] = {}

	return user_dict