use admin
db.createUser({
	user:'admin',
	pwd:'abc123456',
	roles:[{role:'root',db:'admin'}]
})