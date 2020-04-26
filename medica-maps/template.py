import json

# code = {
#     "AN":"Andaman and Nicobar Island",
#     "AP":"Andhra Pradesh",
#     "AR":"Arunachal Pradesh",
#     "AS":"Assam",
#     "BR":"Bihar",
#     "CG":"Chandigarh",
#     "CH":"Chhattisgarh",
#     "DN":"Dadra and Nagar Haveli",
#     "DD":"Daman and Diu",
#     "DL":"Delhi",
#     "GA":"Goa",
#     "GJ":"Gujarat",
#     "HR":"Haryana",
#     "HP":"Himachal Pradesh",
#     "JK":"Jammu and Kashmir",
#     "JH":"Jharkhand",
#     "KA":"Karnataka",
#     "KL":"Kerala",
#     "LA":"Ladakh",
#     "LD":"Lakshadweep",
#     "MP":"Madhya Pradesh",
#     "MH":"Maharashtra",
#     "MN":"Manipur",
#     "ML":"Meghalaya",
#     "MZ":"Mizoram",
#     "NL":"Nagaland",
#     "OR":"Odisha",
#     "PY":"Puducherry",
#     "PB":"Punjab",
#     "RJ":"Rajasthan",
#     "SK":"Sikkim",
#     "TN":"Tamil Nadu",
#     "TS":"Telangana",
#     "TR":"Tripura",
#     "UP":"Uttar Pradesh",
#     "UK":"Uttarakhand",
#     "WB":"West Bengal"
# }


# code = {k: k for k, v in code.items()}
# print(code)

with open('data.json', 'r') as f:
    data = json.load(f)
col = {}
for row in data:
    col[row['State/UT/Division']]= {
        "name": row['State/UT/Division'],
        'ruralH': row['Number of Rural Hospitals (Govt.)'],
        'ruralB': row['Number of beds in Rural Hospitals (Govt.)'],
        'urbanH': row['Number of Urban Hospitals (Govt.)'],
        'urbanB': row['Number of beds in Urban Hospitals (Govt.)'],
        'hospitals': row['Number of Total Hospitals (Govt.)'],
        'hospitalB': row['Number of beds in Total Hospitals (Govt.)'],
        'population': row['Provisional/ Projected Population as on reference period in (000)'],
        'avgPGH': row['Average Population Served Per Govt. Hospital'],
        'avgPGHB': row['Average Population Served Per Govt. Hospital Bed'],
        'reference': row['Reference Period']
    }


with open('geo.json', 'w') as f:
    json.dump(col, f)
