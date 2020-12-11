<!--
 * @Author: rainyl
 * @Date: 2020-12-11 15:24:50
 * @LastEditTime: 2020-12-11 15:37:13
 * @Description: readme file
 * @FilePath: \shark2nayang\README.md
-->

# 鲨鱼记账数据库转那样记账数据库文件

## 鲨鱼记账数据库文件位置

对于`安卓版`鲨鱼记账数据库位于安卓系统`/data/data/com.shark.jizhang/database`,其中，用户记账数据
的数据库为`shark_account.db`,为`SQLite3`数据库格式，目前暂未加密（2020.12.11）。

## 那样记账

- 使用备份恢复功能，先设置好软件，不要添加记账记录，程序运行中会直接Drop掉记账记录表。

- 设置好软件之后，备份数据到文件，为`ZIP`文件，导出到电脑上
- 运行`python main.py -s SOURCE_DB_FILE -d DESTINATION_DB_FILE`即可将鲨鱼记账的记账记录导入那样记账数据库
- 将得到的新数据库替换原备份文件中的数据库，导入手机，恢复即可

## 注意事项

- 不需要额外库，安装python即可

## LICENSE

暂时不设置
