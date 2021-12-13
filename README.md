# database-sqlserver-
hust数据库实验

#### 安装环境
  sqlserver
  SMSS

#### 使用须知
  需要开启sql server 身份验证
  需要创建数据库实例
  使用如下命令创建初始基本表格
  
  create table Student
  (Sno CHAR(9) PRIMARY KEY,
  Sname CHAR(20) UNIQUE,
  Ssex CHAR(2),
  Sage SMALLINT,
  Sdept CHAR(20),
  Scholarship char(2)
  );
  go
  (Cno CHAR(4) PRIMARY KEY,
  Cname CHAR(40),
  Cpno CHAR(4),
  Ccredit SMALLINT,
  FOREIGN KEY (Cpno) REFERENCES Course(Cno)
  );
  go
  create table SC
  (Sno CHAR(9),
  Cno CHAR(4),
  Grade SMALLINT,
  primary key (Sno, Cno),
  FOREIGN KEY (Sno) REFERENCES Student(Sno),
  FOREIGN KEY (Cno) REFERENCES Course(Cno)
  );
  go
  
#### 特别注意在
