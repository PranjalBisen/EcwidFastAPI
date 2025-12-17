import os
import requests
from fastapi import FastAPI,HTTPException

app=FastAPI()

ecwid_token=os.getenv("ecwid_token")
ecwid_storeid=os.getenv("ecwid_storeid")
baseurl=f"https://app.ecwid.com/api/v3/{ecwid_storeid}"

def auth_header():
    return {"Authorization":f"Bearer {ecwid_token}"}

def get_order():
    resp=requests.get(f"{baseurl}/orders",headers=auth_header(),timeout=5)
    if resp.status_code!=200:
        raise HTTPException(status_code=502,detail="order api failed")
    return resp.json().get("items",[])

def get_prod():
    resp=requests.get(f"{baseurl}/products",headers=auth_header(),timeout=5)
    if resp.status_code!=200:
        raise HTTPException(status_code=502,detail="product api failed")
    return resp.json().get("items",[])

#On shelf products
@app.get("/products/on_shelf")
def on_shelf():
    orders=get_order()
    products=get_prod()

    sett=set()
    for i in orders:
        for j in i.get("items",[]):
            id=j.get("productId")
            if id is not None:
                sett.add(id)

    ans=[]
    for i in products:
        if i.get("id") in sett:
            ans.append({"id":i.get("id"),"name":i.get("name")})
    return {"items":ans}

# #Not on shelf products
# @app.get("/products/not_on_shelf")
# def not_on_shelf():
#     orders=get_order()
#     products=get_prod()

#     sett=set()
#     for i in orders:
#         for j in i.get("items",[]):
#             id=j.get("productId")
#             if id is not None:
#                 sett.add(id)

#     ans=[]
#     for i in products:
#         if i.get("id") not in sett:
#             ans.append({"id":i.get("id"),"name":i.get("name")})
#     return {"items":ans}

# #Prodcuts atleast k times ordered
# @app.get("/products/orders/at_least/{k}")
# def at_least_k(k:int):
#     orders=get_order()
#     products=get_prod()

#     mp={}
#     for i in orders:
#         for j in i.get("items",[]):
#             id=j.get("productId")
#             if id is None:
#                 continue
#             if id not in mp:
#                 mp[id]=1
#             else:
#                 mp[id]+=1

#     ans=[]
#     for i in products:
#         id=i.get("id")
#         if mp.get(id,0)>=k:
#             ans.append({"id":id,"name":i.get("name")})
#     return {"items":ans}

# #Products at most k times ordered
# @app.get("/products/orders/at_most/{k}")
# def at_most_k(k:int):
#     orders=get_order()
#     products=get_prod()

#     mp={}
#     for i in orders:
#         for j in i.get("items",[]):
#             id=j.get("productId")
#             if id is None:
#                 continue
#             if id not in mp:
#                 mp[id]=1
#             else:
#                 mp[id]+=1

#     ans=[]
#     for i in products:
#         id=i.get("id")
#         if mp.get(id,0)<=k:
#             ans.append({"id":id,"name":i.get("name")})
#     return {"items":ans}
