import json
#from app.models import User, Message

class OurJsonEncoder(json.JSONEncoder):
	def default(self, o):
		#for cl in [User, Message]:
		#	if isinstance(o, cl):
		#		return o.to_dict()
		json.JSONEncoder.default(self, o)

json_encoder = OurJsonEncoder()
jenc = json_encoder.encode