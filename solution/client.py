import requests
url = "http://localhost:8000/characters"
new_character = {
    "name":"Gandalf",
    "level":10,
    "rol":"Wizard",
    "charisma":15,
    "strength":10,
    "dexterity":10,
}
response = requests.request(method="POST",url=url,json=new_character)
print(response.text)

response = requests.request(method="GET",url=url)
print(f"\n{response.text}",)

response = requests.request(method="GET",url=url+"/1")
print(f"\n{response.text}",)


new_character = {
    "name":"Robin",
    "level":"5",
    "rol":"Archer",
    "charisma":10,
    "strength":10,
    "dexterity":10,
}
response = requests.request(method="POST",url=url,json=new_character)

new_character = {
    "name":"Aragorn",
    "level":10,
    "rol":"Warrior",
    "charisma":"20",
    "strength":15,
    "dexterity":15,
}
response = requests.request(method="POST",url=url,json=new_character)

response = requests.request(method="GET",url=url+"/?rol=Archer&level=5&charisma=10")
print(f"\n{response.text}")

update_character = {
    "charisma":10,
    "strength":15,
    "dexterity":15
}
response = requests.request(method="PUT",url=url+"/3",json=update_character)
print(f"\n{response.text}",)

new_character = {
    "name":"Aragon",
    "level":10,
    "rol":"Warrior",
    "charisma":"20",
    "strength":15,
    "dexterity":15,
}
response = requests.request(method="POST",url=url,json=new_character)

response = requests.request(method="DELETE",url=url+"/3")
print(f"\n{response.text}",)

new_character = {
    "name":"Legolas",
    "level":"5",
    "rol":"Archer",
    "charisma":15,
    "strength":10,
    "dexterity":10,
}
response = requests.request(method="POST",url=url,json=new_character)

response = requests.request(method="GET",url=url,json=update_character)
print(f"\n{response.text}",)


























