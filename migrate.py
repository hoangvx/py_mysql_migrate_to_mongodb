import yaml
import mysql.connector
import datetime

from pymongo import MongoClient

# read db config
with open("db.yml", "r") as ymlFile:
  config = yaml.load(ymlFile)

# read migration transaction config
with open("tr.yml", "r") as ymlFile:
  tr = yaml.load(ymlFile)


mysql_conn = mysql.connector.connect(
  user=config["mysql"]["username"],
  password=config["mysql"]["password"],
  host=config["mysql"]["host"],
  database=config["mysql"]["database"]
)

cursor = mysql_conn.cursor()

mongo_conn = MongoClient(config["mongodb"]["host"], 27017)

db = eval("mongo_conn.%s" % (config["mongodb"]["database"]))


  
for table, props in tr.iteritems():
  if "embed" not in props or props["embed"] == False:
    query = "SELECT {} FROM {}".format(", ".join(props["columns"]), table)
    cursor.execute(query)
    for row in cursor:
      dic = { col: row[idx].strftime('%m/%d/%Y') if isinstance(row[idx], datetime.datetime) else row[idx] for idx, col in enumerate(props["columns"]) }
      result = eval("db.{0}.insert_one({1})".format(table, dic))

for table, props in tr.iteritems():
  if "embed" in props and props["embed"]:
    query = "SELECT {} FROM {}".format(", ".join(props["columns"]), table)
    cursor.execute(query)
    key = props["embed"]["key"]
    fr = props["embed"]["from"]

    for row in cursor:
      dic = { col: row[idx] for idx, col in enumerate(props["columns"]) }
      print(dic)
      s = """db.{0}.update(
        {{
          "{2}": dic["{2}"]
        }},
        {{
          "$push": {{
            "{1}" : dic
          }}
        }}
      )""".format(fr, table, key)
      eval(s)
      


cursor.close()
mysql_conn.close()
