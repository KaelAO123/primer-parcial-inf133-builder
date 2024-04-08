
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
import json
characters={}
class HTTPRequestHandler:
    @staticmethod
    def http_response(handler,status,data):
        handler.send_response(status)
        handler.send_header("Content-type","Application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def http_read(handler):
        content_length=int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))

class Character:
    name = None
    level = None
    rol = None
    charisma = None
    strength = None
    dexterity = None

class CharacterBuilder:
    def __init__(self):
        self.character = Character()
    
    def set_name(self,name):
        self.character.name = name

    def set_level(self,level):
        self.character.level = level
        
    def set_rol(self,rol):
        self.character.rol = rol
    
    def set_charisma(self,charisma):
        self.character.charisma = charisma
    
    def set_strength(self,strength):
        self.character.strength = strength

    def set_dexterity(self,dexterity):
        self.character.dexterity = dexterity
    
    def get_character(self):
        return self.character

class CharacterService:
    def __init__(self):
        self.builder = CharacterBuilder()
    
    @staticmethod
    def find_character(id):
        ide = str(id)
        if id in characters:
            return {id: characters[id].__dict__}
        return None
        
    @staticmethod
    def create_character(data):
        new_character = CharacterBuilder()
        new_character.set_name(data.get("name",None))
        new_character.set_level(data.get("level",None))
        new_character.set_rol(data.get("rol",None))
        new_character.set_charisma(data.get("charisma",None))
        new_character.set_strength(data.get("strength",None))
        new_character.set_dexterity(data.get("dexterity",None))

        characters[len(characters)+1] = new_character.get_character()
        return new_character.get_character().__dict__
    
    @staticmethod
    def list_characters():
        return {index:character.__dict__ for index,character in characters.items()}
    
    @staticmethod
    def attributes_characters(rol,level,charisma):
        return {index:character.__dict__ for index,character in characters.items() if character.rol==rol and character.level==level and character.charisma==charisma}

    @staticmethod
    def update_characters(id,data):
        character = CharacterService.find_character(id)
        if character:
            characters[id].__dict__.update(data)
            return characters[id].__dict__
        else:
            return None
        
    @staticmethod
    def delete_character(id):
        character = CharacterService.find_character(id)
        if character:
            del characters[id]
            return {"message":"Character deleted successfully"}
        else:
            return None
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parse_path = urlparse(self.path)
        query_params = parse_qs(parse_path.query)
        if parse_path.path == "/characters":
            list_characters = CharacterService.list_characters()
            HTTPRequestHandler.http_response(self,201,list_characters)
        elif self.path.startswith("/characters/"):
            if "rol" in query_params and "level" in query_params and "charisma" in query_params:
                rol = query_params.get("rol")[0]
                level = query_params.get("level")[0]
                charisma = query_params.get("charisma")[0]
                rol_character = CharacterService.attributes_characters(rol,level,charisma)
                if rol_character:
                    HTTPRequestHandler.http_response(self,201,rol_character)
                else:
                    HTTPRequestHandler.http_response(self,404,{"Error":"Rol no encontrado"})
            else:
                id = int(self.path.split("/")[-1])
                id_character = CharacterService.find_character(id)
                if id_character:
                    HTTPRequestHandler.http_response(self,201,id_character)
                else:
                    HTTPRequestHandler.http_response(self,404,{"Error":"No hay"})
        else:
            HTTPRequestHandler.http_response(self,404,{"Error":"Ruta no existente"})

    def do_POST(self):
        if self.path == "/characters":
            data = HTTPRequestHandler.http_read(self)
            created_character = CharacterService.create_character(data)
            if created_character:
                HTTPRequestHandler.http_response(self,201,created_character)
            else:
                HTTPRequestHandler.http_response(self,404,{"Error":"Personaje no creado"})
    
    def do_PUT(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[-1])
            data = HTTPRequestHandler.http_read(self)
            update_character = CharacterService.update_characters(id,data)
            if update_character:
                HTTPRequestHandler.http_response(self,201,update_character)
            else:
                HTTPRequestHandler.http_response(self,201,{"Error":"Personaje no actualizado"})

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            id = int(self.path.split("/")[-1])
            delate_character = CharacterService.delete_character(id)
            if delate_character:
                HTTPRequestHandler.http_response(self,201,delate_character)
            else:
                HTTPRequestHandler.http_response(self,201,{"Error":"Personaje no eliminado"})

def main(port=8000):
    try:
        server_address = ("",port)
        httpd = HTTPServer(server_address,RequestHandler)
        print(f"Iniciando servidor en: http://localhost:{port}")
        httpd.serve_forever()
    except:
        print("Cerrando servidor")
        httpd.socket.close()

if __name__ == "__main__":
    main()