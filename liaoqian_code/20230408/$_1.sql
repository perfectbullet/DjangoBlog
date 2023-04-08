use school
/*
db.student.find({
    age:{$gte:20,$lte:30}
})

db.student.find({
    city:{$nin:['苏州市','大连市']}
})
*/
db.student.find({name:{$ne:'李强'}})