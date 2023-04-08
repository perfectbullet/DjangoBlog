use school

//查询身份是班主任和年级主任的教师
//db.teacher.save({name:'Jack',role:['班主任','年级主任','副校长']})
//db.teacher.find({role:{$all:['班主任','年级主任']}})
//查询年龄不在28-30岁之间的学生
/*
db.student.find({
    age:{$not:{$gte:28,$lte:30}}
})
*/
//查询30岁以下的男学生,或者25岁以下的女学生
//db.student.find({$or:[{age:{$lt:30},sex:'男'},{age:{$lt:25},sex:'女'}]})
//查询含有age字段的学生
db.student.find({age:{$exists:1}})