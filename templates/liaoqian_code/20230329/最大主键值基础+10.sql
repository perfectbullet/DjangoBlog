INSERT INTO t_dept(deptno,dname,loc)
VALUES((SELECT MAX(deptno) FROM t_dept)+10,"A部门","北京");

DELETE FROM t_dept WHERE deptno IN (50,60);
INSERT INTO t_dept 
(SELECT MAX(deptno)+10,"A部门","北京" FROM t_dept UNION
SELECT MAX(deptno)+20,"B部门","上海" FROM t_dept);