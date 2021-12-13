import cmd
import pymssql

class wsxk_cmd(cmd.Cmd):
    prompt = 'wsxk>'
    intro = 'welcome to wxk database!'
    wxk_database = None
    cursor = None

    def __init(self):
        cmd.Cmd.__init__(self)

    def do_exit(self,arg):
        'usage:close the program'
        print('bye~')
        return True

    def do_connect(self,arg):
        'usage:connect database'
        self.wxk_database = pymssql.connect('LAPTOP-ATJR7M60', 'wsxk', 'wu123456', 'S_T_U201911737')
        if self.wxk_database:
            print("connect successfully!")
            self.cursor = self.wxk_database.cursor()
        else:
            print("connect error! try again!")

    def do_addstuinfo(self,arg):
        'usage: addstuinfo Sno Sname Ssex Sage Sdept Scholarship'
        try:
            args = arg.split()
            sql = "insert into Student values("
            length = len(args)
            for i in range(length):
                if i != (length-1):
                    sql += args[i]+","
                else:
                    sql += args[i]+")"
            print(sql)
            self.cursor.execute(sql)   #执行sql语句
            self.wxk_database.commit()  #提交
            print("add successfully!")
        except Exception as e:
            print(e)
            #print("error: maybe the info has already exist in table!")
    
    def do_editstuinfo(self,arg):
        "usage: editstuinfo Sno [attribute=value]* \nexample: do_editstuinfo 20001009 Sage=12 \n note:value must be accorded with the attribute type! \nexample:Sname='abc'"
        try:
            args = arg.split()
            sql = 'update Student set '
            length = len(args) 
            for i in range(1,length):
                if i!=(length-1):
                    sql += args[i]+','
                else:
                    sql += args[i]+ ' where Sno='+args[0]
            #print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()
        except Exception as e:
            print(e)
            #print("format error!please use 'help editstuinfo' for more information")    

    def do_addnewcourse(self,arg):
        "usage: add new course info\n example:addnewcourse Cno Cname Cpno Ccredit"
        try:
            args = arg.split()
            length = len(args)
            sql = "insert into Course values("
            for i in range(length):
                if i != (length-1):
                    sql += args[i]+","
                else:
                    sql += args[i]+")"
            print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()
        except Exception as e:
            print(e)

    def do_editcourseinfo(self,arg):
        "usage: editcourseinfo Cno [attribute=value]* \nexample: editcourseinfo 8 Ccredit=8 \n note:value must be accorded with the attribute type! \nexample:Cname='abc'"
        try:
            args = arg.split()
            sql = 'update Course set '
            length = len(args)
            for i in range(1,length):
                if i!=(length-1):
                    sql += args[i]+','
                else:
                    sql += args[i]+ ' where Cno='+args[0]
            print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()                
        except Exception as e:
            print(e)
    
    def do_delcourse(self,arg):
        "usage: delcourse Cno\n example: delcourse 8"
        try:
            args = arg.split()
            sql = "delete from Course where Cno="+args[0]
            print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()
            print("delete successfully")
        except Exception as e:
            print(e)

    def do_addstuscore(self,arg):
        "usage: addstuscore Sno Cno Grade\n example: addstuscore 200215121 3 95"
        try:
            args=arg.split()
            length = len(args)
            sql = "insert into SC values("
            for i in range(length):
                if i != (length-1):
                    sql += args[i]+","
                else:
                    sql += args[i]+")"
            print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()
        except Exception as e:
            print(e)

    def do_editstuscore(self,arg):
        "usage: editstuscore Sno Cno [attribute=value]* \nexample: editstuscore 200215121 1 Grade=30 \n note:value must be accorded with the attribute type! \nexample:Grade=30"
        try:
            args = arg.split()
            sql = 'update SC set '
            length = len(args)
            for i in range(2,length):
                if i!=(length-1):
                    sql += args[i]+','
                else:
                    sql += args[i]+ ' where Sno='+args[0]+" and "+"Cno="+args[1]
            print(sql)
            self.cursor.execute(sql)
            self.wxk_database.commit()                
        except Exception as e:
            print(e)

    def do_statisticsasdept(self,arg):
        "usage:statisticsasdept Sdept Cno\n example:statisticsasdept 'CS' 1"
        try:
            bad=0
            good=0
            args = arg.split()
            # get number
            sql = "select Grade from Student,SC where Sdept="+args[0]+" and SC.Sno=Student.Sno and SC.Cno ="+ args[1]
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            length = len(data)
            total = length
            for i in range(length):
                if data[i][0]>=90:
                    good+=1
                if data[i][0]<60:
                    bad+=1
            
            sql = "select avg(Grade),max(Grade),min(Grade) from Student,SC where Sdept="+args[0]+" and SC.Sno=Student.Sno and SC.Cno ="+ args[1]
            #print(sql)
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            #print(good,total)
            print("avg:%d max:%d min:%d good rate:%.2f bad num:%d"%(data[0],data[1],data[2],float(good)/float(total),bad))               
        except Exception as e:
            print(e)        
    
    def do_statisticsrank(self,arg):
        "usage:statisticsrank Sdept Cno\n example:statisticsrank 'CS' 2"
        try:
            args=arg.split()
            sql = "select Cname,Ccredit from Course where Cno="+args[1]
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            print(data[0].encode('latin-1').decode('gbk').strip(),"学分: %d"%data[1])
            
            sql = "select Student.Sname,Grade from Student,SC where Student.Sdept="+args[0]+" and Student.Sno=SC.Sno and SC.Cno ="+args[1] +" order by Grade DESC"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            length = len(data)
            for i in range(length):
                print(data[i][0].encode('latin-1').decode('gbk').strip()," "+str(data[i][1]))
        except Exception as e:
            print(e)

    def do_searchstuinfo(self,arg):
        "usage:searchstuinfo Sno\n example:searchstuinfo 20001009"
        try:
            args = arg.split()
            sql = "select * from Student where Sno="+args[0]
            self.cursor.execute(sql)
            data = self.cursor.fetchone()
            print("Sname:"+data[1].encode('latin-1').decode('gbk').strip()," Ssex:"+data[2].encode('latin-1').decode('gbk').strip()," Sage:"+str(data[3]).strip()," Sdept:"+data[4].encode('latin-1').decode('gbk').strip()," Scholarship:"+data[5].encode('latin-1').decode('gbk').strip())

            print("选修课程:")
            sql = "select Course.Cname,Course.Ccredit from SC,Course where SC.Sno="+args[0]+" and Course.Cno=SC.Cno"
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            length = len(data)
            for i in range(length):
                print(data[i][0].encode('latin-1').decode('gbk').strip()," Ccredit:"+str(data[i][1]))
        except Exception as e:
            print(e)