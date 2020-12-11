import sqlite3
import os
import datetime
from argparse import ArgumentParser

ASSETS_HASH = {
    "餐饮": 1,
    "零食": 2,
    "水果": 3,
    "日用": 4,
    "交通": 5,
    "住房": 6,
    "水电": 7,
    "服饰": 8,
    "购物": 9,
    "娱乐": 10,
    "电影": 11,
    "门票": 12,
    "数码": 13,
    "美妆": 14,
    "理发": 15,
    "医疗": 16,
    "红包": 17,
    "母婴": 18,
    "孩子": 18,
    "宠物": 19,
    "话费": 20,
    "人情": 21,
    "学习": 22,
    "保险": 23,
    "捐赠": 24,
    "恋爱": 25,
    "亏损": 26,
    "薪资": 27,
    "工资": 27,
    "奖金": 28,
    "红包1": 29,
    "收益": 30,
    "兼职": 31,
    "礼物": 32,
    "通讯": 33,
    "其它": 34,
}


def init_nayang(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE `Assets` (`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                "`name` TEXT NOT NULL, "
                "`img_name` TEXT NOT NULL, "
                "`type` INTEGER NOT NULL, "
                "`state` INTEGER NOT NULL, "
                "`remark` TEXT NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`money` INTEGER NOT NULL, "
                "`ranking` INTEGER, "
                "`init_money` INTEGER NOT NULL, "
                "`total_amount` INTEGER, "
                "`card_num` TEXT, "
                "`billing_day` TEXT, "
                "`repayment_day` TEXT, "
                "`remind` INTEGER, "
                "`add_amount` INTEGER, "
                "`bg_image` TEXT, "
                "`borrow_date` INTEGER, "
                "`return_date` INTEGER)"
                )
    cur.execute("CREATE TABLE `AssetsModifyRecord` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                "`state` INTEGER NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`assets_id` INTEGER NOT NULL, "
                "`money_before` INTEGER NOT NULL, "
                "`money` INTEGER NOT NULL, "
                "FOREIGN KEY(`assets_id`) REFERENCES `Assets`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE )"
                )
    cur.execute("CREATE TABLE `AssetsTransferRecord` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                "`state` INTEGER NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`time` INTEGER NOT NULL, "
                "`assets_id_form` INTEGER NOT NULL, "
                "`assets_id_to` INTEGER NOT NULL, "
                "`remark` TEXT NOT NULL, "
                "`money` INTEGER NOT NULL, "
                "FOREIGN KEY(`assets_id_form`) REFERENCES `Assets`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE , "
                "FOREIGN KEY(`assets_id_to`) REFERENCES `Assets`(`id`) ON UPDATE NO ACTION ON DELETE CASCADE )"
                )
    cur.execute("CREATE TABLE `Budget` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                "`badge` INTEGER NOT NULL, "
                "`type` INTEGER NOT NULL, "
                "`record_type_id` INTEGER NOT NULL, "
                "`assets_id` INTEGER, "
                "`state` INTEGER NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`ranking` INTEGER, "
                "FOREIGN KEY(`record_type_id`) REFERENCES `RecordType`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION )"
                )
    cur.execute("CREATE TABLE `DebtRecord` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                "`state` INTEGER NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`time` INTEGER, "
                "`assets_id_form` INTEGER, "
                "`assets_id_to` INTEGER, "
                "`remark` TEXT, "
                "`type` INTEGER, "
                "`money` INTEGER NOT NULL)"
                )
    cur.execute("CREATE TABLE `Label` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                "`name` TEXT NOT NULL, "
                "`state` INTEGER NOT NULL, "
                "`create_time` INTEGER NOT NULL, "
                "`ranking` INTEGER)"
                )
    cur.execute("CREATE TABLE `Record` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                "`money` INTEGER, "
                "`remark` TEXT, "
                "`time` INTEGER, "
                "`create_time` INTEGER, "
                "`record_type_id` INTEGER NOT NULL, "
                "`assets_id` INTEGER, "
                "FOREIGN KEY(`record_type_id`) REFERENCES `RecordType`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION )"
                )
    cur.execute("CREATE TABLE `RecordType` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                "`name` TEXT, "
                "`img_name` TEXT, "
                "`type` INTEGER NOT NULL, "
                "`ranking` INTEGER NOT NULL, "
                "`state` INTEGER NOT NULL, "
                "`assets_id` INTEGER)"
                )
    cur.execute("CREATE TABLE android_metadata (locale TEXT)")
    cur.execute("CREATE TABLE room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT)")
    conn.commit()
    conn.close()


def init_nayang_from_exist(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("drop table Record;")
    cur.execute("CREATE TABLE `Record` "
                "(`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                "`money` INTEGER, "
                "`remark` TEXT, "
                "`time` INTEGER, "
                "`create_time` INTEGER, "
                "`record_type_id` INTEGER NOT NULL, "
                "`assets_id` INTEGER, "
                "FOREIGN KEY(`record_type_id`) REFERENCES `RecordType`(`id`) ON UPDATE NO ACTION ON DELETE NO ACTION )"
                )
    conn.commit()
    conn.close()


def save_nayang(db_path, sk_data):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executemany(
        "insert into Record(money,remark,time,create_time,record_type_id,assets_id) values(?,?,?,?,?,?);",
        sk_data
    )
    conn.commit()
    conn.close()


def process_shark_data(sk_data):
    sk_data_new = []
    for i, r in enumerate(sk_data):
        rr = [r[0]*100, r[1]]
        act_time = datetime.datetime(year=int(r[2]), month=int(r[3]), day=int(r[4])).timestamp()
        rr.extend([int(act_time*1000), r[5], ASSETS_HASH[r[-2]], -1])
        sk_data_new.append(rr)
    return sk_data_new


def read_shark(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # get account,remark,ctime,ctime,category_name
    cur.execute("select account,remark,year,month,day,ctime,category_name,-1 from account_category_detail")
    account_detail = cur.fetchall()
    return account_detail


def main(_from_db, _to_db):
    act_detail = read_shark(_from_db)
    sk_data = process_shark_data(act_detail)
    # init_nayang(_to_db)
    init_nayang_from_exist(_to_db)
    save_nayang(_to_db, sk_data)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--source', '-s', help="source database(shark jizhang)")
    parser.add_argument('--destination', '-d', help="destination database (nayang wallet)")

    args = parser.parse_args()
    from_db = args.source
    to_db = args.destination
    main(from_db, to_db)
