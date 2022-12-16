import genson
import xmltodict
import pandas as pd

global count
count = 0

def parse_schema(schema_dict, parent, schema, current_path):
    global count
    # count = 0
    if isinstance(schema_dict, list):
        schema_dict = schema_dict[0]
    for key in schema_dict:
        if key == "required":
            continue
        print('---', key)
        if key == "items":
            count = count + 1
            schema.append(
                {
                    "key": parent + str(count) if parent == "items" else parent,
                    "display_name": parent + str(count) if parent == "items" else parent,
                    "format": "array",
                    "description": "",
                    "parent": "",
                    "array_field": "items" + str(count),
                    "path": current_path,
                    "parent_path": ".".join(current_path.split('.')[0:-1])
                }
            )
            parse_schema(schema_dict["items"], key, schema, current_path)
            continue
        if key == "type":
            continue

        if key == "properties":
            path = current_path + ".items" if parent == "items" else current_path
            schema.append(
                {
                    "key": parent + str(count) if parent == "items" else parent,
                    "display_name": parent + str(count) if parent == "items" else parent,
                    "format": "json",
                    "description": "",
                    "parent": "",
                    "array_field": "",
                    "path": path,
                    "parent_path": ".".join(path.split('.')[0:-1])
                }
            )
            parse_schema(schema_dict["properties"], parent, schema, path)
            continue
        if "type" in schema_dict[key] and schema_dict[key]["type"] not in [
            "array",
            "object",
        ]:
            schema.append(
                {
                    "key": key,
                    "display_name": key,
                    "format": "string",
                    "description": "",
                    "parent": parent + str(count) if parent == "items" else parent,
                    "array_field": "",
                    "path": current_path + "." + key,
                    "parent_path": current_path
                }
            )
        else:
            parse_schema(schema_dict[key], key, schema, current_path + "." + key)


# with open('/home/abhinav/data/data_aqi_cpcb.xml') as xmlFile:

#     builder = genson.SchemaBuilder()
#     jsondata = xmltodict.parse(xmlFile.read(), xml_attribs=True)
#     # print (jsondata)
#     # jsondata = json.loads(
#     #     jsonFile.read()
#     # )   json.loads(resource.filedetails.file)
#     builder.add_object(jsondata)
#     schema_dict = builder.to_schema()
#     # print (schema_dict)
#     schema_dict = schema_dict.get("properties", schema_dict.get("items", {}).get("properties", {})) #schema_dict.get("properties", {})
#     schema = []
#     parse_schema(schema_dict, "", schema, "")
#     print (schema)


# df = pd.read_csv('/home/abhinav/data/test.csv')
# df['date']= pd.to_datetime(df['date'])

# schema_list = pd.io.json.build_table_schema(df, version=False)
# schema_list = schema_list.get("fields", [])
# print (schema_list)

xml = '''<?xml version='1.0' encoding='utf-8'?>
<data xmlns="http://example.com">
 <row>
   <shape>square</shape>
   <degrees>360</degrees>
   <sides>4.0</sides>
 </row>
 <row>
   <shape>circle</shape>
   <degrees>360</degrees>
   <sides/>
 </row>
 <row>
   <shape>triangle</shape>
   <degrees>180</degrees>
   <sides>3.0</sides>
 </row>
</data>'''

# json = '{"row 1":{"col 1":"a","col 2":"b"},"row 2":{"col 1":"c","col 2":"d"}}'
json = '[{"col 1":"a","col 2":"b"},{"col 1":"c","col 2":"d"}]'

# df = pd.read_xml(r'/home/abhinav/data/test_xml.xml')
df = pd.read_json(json)
print (df)