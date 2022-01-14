from json.decoder import JSONDecodeError
import json
import os
import re
import time
from xml.dom import minidom
from  abc import ABC, abstractmethod

from genesis_tools import genesis_games_data

SETTINGS_PATH = './nes_conf.json'
SYSTEM = 'nes'

UNIX_PATH = '/'

default_settings = {
    "games_lang":       'en',
    "games_dir":        '.',
    "images_dir":       'images',
    "manuals_dir":      'manuals',
    "videos_dir":       'videos',
    "gamelist":         "gamelist.xml",
    "gamedata":         "gamedata.json",
    "game_types":       "",
    "image_types":      "(.png|.jpg|.jpeg|.tiff|.gif)$",
    "video_types":      "(.mp4|.avi)$",
    "manual_types":     "(.pdf)$",
    "path":             "",
    "system":           "",
}

class Processor(ABC):

    @abstractmethod
    def load_settings(self):
        pass

class GamesListProcessor(Processor):
    CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGES_DIR = 'images'
    MANUALS_DIR = 'manuals'
    VIDEOS_DIR = 'videos'
    GAMES_DIR = '.'

    XML_FILE_NAME = 'gamelist.xml'
    GAMEDATA_FILE_NAME = 'gamedata.json'

    GAMES_LANG = 'en'

    IMAGE_TYPES = r"(.png|.jpg|.jpeg|.tiff|.gif)$"
    VIDEO_TYPES = r"(.mp4|.avi)$"
    MANUAL_TYPES = r"(.pdf)$"
    GAME_TYPES = r""

    def __init__(self, settings_path, system):
        self.settings_path  =   settings_path
        self.settings       =   self.load_settings()

        self.path           =   self.settings.get('path', self.CURRENT_PATH)
        self.games_lang     =   self.settings.get('games_lang', self.GAMES_LANG)        
        self.games_dir      =   self.settings.get('games_dir', self.GAMES_DIR)
        self.images_dir     =   self.settings.get('images_dir', self.IMAGES_DIR)        
        self.manuals_dir    =   self.settings.get('manuals_dir', self.MANUALS_DIR)            
        self.videos_dir     =   self.settings.get('videos_dir', self.VIDEOS_DIR)        
        self.gamelist_path  =   self.settings.get('gamelist', self.XML_FILE_NAME)        
        self.gamedata_path  =   self.settings.get('gamedata', self.GAMEDATA_FILE_NAME)        
        self.game_types     =   self.settings.get('game_types', self.GAME_TYPES)        
        self.image_types    =   self.settings.get('image_types', self.IMAGE_TYPES)            
        self.video_types    =   self.settings.get('video_types', self.VIDEO_TYPES)            
        self.manual_types   =   self.settings.get('manual_types', self.MANUAL_TYPES)            
        self.system         =   self.settings.get('system', system)

        self.games_files     =   []
        self.images_files    =   []
        self.manuals_files   =   []
        self.videos_files    =   []

        self.gamelist_obj   =   None
        self.gamelist_str   =   ''

        self.games_data      =   []
        
        
    def load_settings(self):
        settings = {}
        try:
            with open(self.settings_path, "r") as settings_file:
                settings = json.load(settings_file)

        except FileNotFoundError as not_found_ex:
            print(f"[ERROR] Settings file not found ({self.settings_path}) | {not_found_ex}")
        except IOError as not_found_ex:
            print(f"[ERROR] Settings file not found ({self.settings_path}) | {not_found_ex}")
        except JSONDecodeError as decode_ex:
            print(f"[ERROR] Can't read settings file | {decode_ex}")
        else:
            print("[INFO] Settings successfully loaded")

        self.settings = {**default_settings, **settings}

        print(f"[INFO] SETTINGS:")
        print(self.settings)

        return self.settings

    def write_gamelist_xml(self, xml_string=None):
        data_to_write = xml_string or self.gamelist_str

        data_to_write = re.sub(r"(&)", '&amp;', data_to_write)

        with open(os.path.join(self.path, self.gamelist_path), 'w', encoding='utf-8') as file:
            file.write(data_to_write)

    def read_gamelist_xml(self, parse=False):
        gamelist_xml_obj = None
        try:
            gamelist_xml_obj = minidom.parse(os.path.join(self.path, self.gamelist_path))
        except Exception as ex:
            print(f"[ERROR] Can't read gameslist file | {ex}")
        else:
            print(f"[INFO] Gamelist file successfuly read")

        self.gamelist_obj = gamelist_xml_obj

        return self.parse_gamelist_obj(gamelist_xml_obj) if parse else self.gamelist_obj

    def parse_gamelist_obj(self, gamelist_obj=None):
        xml_object = gamelist_obj or self.gamelist_obj

        if not xml_object:
            raise ValueError("Can't find XML object")

        games_data = []

        games_from_xml = xml_object.getElementsByTagName('game')

        for game in games_from_xml:
            game_object = {
                "path": '',
                "name": '',
                "image": '',
                "video": '',
                "manual": '',
                "fanart": '',
                "lastplayed": None,
                "playcount": 0,
                "gametime": 0,
                "favorite": False,
                "marquee": '',
                "thumbnail": '',
                "description": '',
                "map": '',
                "rate": '',
                "releasedate": '',
                "developer": '',
                "publisher": '',
                "genres": '',
                "family": '',
                "players": '',
                "md5": '',
                "lang": '',
                "id": '',
            }

            path_tag = game.getElementsByTagName('path') and game.getElementsByTagName('path')[0]
            name_tag = game.getElementsByTagName('name') and game.getElementsByTagName('name')[0]
            image_tag = game.getElementsByTagName('image') and game.getElementsByTagName('image')[0]
            video_tag = game.getElementsByTagName('video') and game.getElementsByTagName('video')[0]
            manual_tag = game.getElementsByTagName('manual') and game.getElementsByTagName('manual')[0]
            fanart_tag = game.getElementsByTagName('fanart') and game.getElementsByTagName('fanart')[0]
            lastplayed_tag = game.getElementsByTagName('lastplayed') and game.getElementsByTagName('lastplayed')[0]
            playcount_tag = game.getElementsByTagName('playcount') and game.getElementsByTagName('playcount')[0]
            gametime_tag = game.getElementsByTagName('gametime') and game.getElementsByTagName('gametime')[0]
            favorite_tag = game.getElementsByTagName('favorite') and game.getElementsByTagName('favorite')[0]
            marquee_tag = game.getElementsByTagName('marquee') and game.getElementsByTagName('marquee')[0]
            thumbnail_tag = game.getElementsByTagName('thumbnail') and game.getElementsByTagName('thumbnail')[0]
            description_tag = game.getElementsByTagName('desc') and game.getElementsByTagName('desc')[0]
            map_tag = game.getElementsByTagName('map') and game.getElementsByTagName('map')[0]
            rate_tag = game.getElementsByTagName('rating') and game.getElementsByTagName('rating')[0]
            releasedate_tag = game.getElementsByTagName('releasedate') and game.getElementsByTagName('releasedate')[0]
            developer_tag = game.getElementsByTagName('developer') and game.getElementsByTagName('developer')[0]
            publisher_tag = game.getElementsByTagName('publisher') and game.getElementsByTagName('publisher')[0]
            genres_tag = game.getElementsByTagName('genre') and game.getElementsByTagName('genre')[0]
            family_tag = game.getElementsByTagName('family') and game.getElementsByTagName('family')[0]
            players_tag = game.getElementsByTagName('players') and game.getElementsByTagName('players')[0]
            md5_tag = game.getElementsByTagName('md5') and game.getElementsByTagName('md5')[0]
            lang_tag = game.getElementsByTagName('lang') and game.getElementsByTagName('lang')[0]


            path_data = path_tag and path_tag.firstChild and path_tag.firstChild.nodeValue or None
            name_data = name_tag and name_tag.firstChild and name_tag.firstChild.nodeValue or None
            image_data = image_tag and image_tag.firstChild and image_tag.firstChild.nodeValue or None
            video_data = video_tag and video_tag.firstChild and video_tag.firstChild.nodeValue or None
            manual_data = manual_tag and manual_tag.firstChild and manual_tag.firstChild.nodeValue or None
            fanart_data = fanart_tag and fanart_tag.firstChild and fanart_tag.firstChild.nodeValue or None
            lastplayed_data = lastplayed_tag and lastplayed_tag.firstChild and lastplayed_tag.firstChild.nodeValue or None
            playcount_data = playcount_tag and playcount_tag.firstChild and playcount_tag.firstChild.nodeValue or None
            gametime_data = gametime_tag and gametime_tag.firstChild and gametime_tag.firstChild.nodeValue or None
            favorite_data = favorite_tag and favorite_tag.firstChild and favorite_tag.firstChild.nodeValue or None
            marquee_data = marquee_tag and marquee_tag.firstChild and marquee_tag.firstChild.nodeValue or None
            thumbnail_data = thumbnail_tag and thumbnail_tag.firstChild and thumbnail_tag.firstChild.nodeValue or None
            description_data = description_tag and description_tag.firstChild and description_tag.firstChild.nodeValue or None
            map_data = map_tag and map_tag.firstChild and map_tag.firstChild.nodeValue or None
            rate_data = rate_tag and rate_tag.firstChild and f"{float(rate_tag.firstChild.nodeValue or 0)*10}/10" or None
            releasedate_data = releasedate_tag and releasedate_tag.firstChild and releasedate_tag.firstChild.nodeValue or None
            developer_data = developer_tag and developer_tag.firstChild and developer_tag.firstChild.nodeValue or None
            publisher_data = publisher_tag and publisher_tag.firstChild and publisher_tag.firstChild.nodeValue or None
            genres_data = genres_tag and genres_tag.firstChild and genres_tag.firstChild.nodeValue or None
            family_data = family_tag and family_tag.firstChild and family_tag.firstChild.nodeValue or None
            players_data = players_tag and players_tag.firstChild and players_tag.firstChild.nodeValue or None
            md5_data = md5_tag and md5_tag.firstChild and md5_tag.firstChild.nodeValue or None
            lang_data = lang_tag and lang_tag.firstChild and lang_tag.firstChild.nodeValue or None
            id_data = game.attributes.get('id') and game.attributes.get('id').value or None

            game_object.update({
                "path": path_data,
                "name": name_data,
                "image": image_data,
                "video": video_data,
                "manual": manual_data,
                "fanart": fanart_data,
                "lastplayed": lastplayed_data,
                "playcount": playcount_data,
                "gametime": gametime_data,
                "favorite": favorite_data,
                "marquee": marquee_data,
                "thumbnail": thumbnail_data,
                "description": description_data,
                "map": map_data,
                "rate": rate_data,
                "releasedate": releasedate_data,
                "developer": developer_data,
                "publisher": publisher_data,
                "genres": [genres_data] if genres_data else [],
                "family": family_data, 
                "players": players_data, 
                "md5": md5_data, 
                "lang": lang_data, 
                "id": id_data, 
            })

            games_data.append(game_object)

        return games_data

    def read_games_files(self):
        files = next(os.walk(os.path.join(self.path, self.games_dir)), (None, None, []))[2] or []
        self.games_files = [file for file in files if re.search(self.game_types, file) != None]
        print(f"[INFO] Games path: {os.path.join(self.path, self.games_dir)}")
        print(f"[INFO] Games files: {self.games_files}")

        return self.games_files

    def read_images_files(self):
        files = next(os.walk(os.path.join(self.path, self.images_dir)), (None, None, []))[2] or []
        self.images_files = [file for file in files if re.search(self.image_types, file) != None]
        print(f"[INFO] Images path: {os.path.join(self.path, self.images_dir)}")
        print(f"[INFO] Images files: {self.images_files}")

        return self.images_files

    def read_videos_files(self):
        files = next(os.walk(os.path.join(self.path, self.videos_dir)), (None, None, []))[2] or []
        self.videos_files = [file for file in files if re.search(self.video_types, file) != None]
        print(f"[INFO] Videos path: {os.path.join(self.path, self.videos_dir)}")
        print(f"[INFO] Videos files: {self.videos_files}")

        return self.videos_files

    def read_manuals_files(self):
        files = next(os.walk(os.path.join(self.path, self.manuals_dir)), (None, None, []))[2] or []
        self.manuals_files = [file for file in files if re.search(self.manual_types, file) != None]
        print(f"[INFO] Manuals path: {os.path.join(self.path, self.manuals_dir)}")
        print(f"[INFO] Manuals files: {self.manuals_files}")

        return self.manuals_files

    def find_image_file_name(self, game_name):
        image_path_str = None
        try:
            image_path_str = next(filter(lambda x: game_name == re.sub(self.image_types, '', x), self.images_files or self.read_images_files()))
        except StopIteration as ex:
            print(f"[WARNING] image for {game_name} not found")
        return image_path_str

    def find_game_data(self, game_name):
        game_data = {}

        try:
            game_data = next(filter(lambda x: game_name == x["name"] or game_name == re.sub(GAME_TYPES, '', x['path']).replace('./',''), self.get_games_data()))
        except StopIteration as ex:
            print(f"[WARNING] game_data for {game_name} not found")

        return game_data
        

    def find_manual_file_name(self, game_name):
        manual_path_str = None
        try:
            manual_path_str = next(filter(lambda x: game_name == re.sub(self.manual_types, '', x), self.manuals_files or self.read_manuals_files()))
        except StopIteration as ex:
            print(f"[WARNING] manual for {game_name} not found")
        return manual_path_str

    def find_video_file_name(self, game_name):
        video_path_str = None
        try:
            video_path_str = next(filter(lambda x: game_name == re.sub(self.video_types, '', x), self.videos_files or self.read_videos_files()))
        except StopIteration as ex:
            print(f"[WARNING] video for {game_name} not found")
        return video_path_str

    def read_games_data(self):
        games_data = []

        try:
            games_data.extend(self.read_gamelist_xml(parse=True))
        except ValueError as value_ex:
            print(f"Can't read gamelist file ({self.gamelist_path}) | {value_ex}")

        try:
            if self.gamedata_path:
                with open(os.path.join(self.path, self.gamedata_path)) as gamedata_file:
                    data = json.load(gamedata_file) or []
                    games_data.extend(data)
        except FileNotFoundError as not_found_ex:
            print(f"[WARNING] Gamesdata file json not found ({self.gamedata_path})")
        except IOError as not_found_ex:
            print(f"[WARNING] Gamesdata file not found ({self.gamedata_path}) | {not_found_ex}")
        except JSONDecodeError as decode_ex:
            print(f"[ERROR] Can't read gamesdata file ({self.gamedata_path}) | {decode_ex}")
        except TypeError as type_ex:
            print(f"[ERROR] Gamesdata file have wrong data format | {type_ex}")
        else:
            print(f"[INFO] Gamesdata successfully read from gamedata file ({self.gamedata_path}) | Length games_data: {len(games_data)}")

        games_data_dict = {}
        for game in games_data:
            game_obj = games_data_dict.get(game['name'], {})

            game_obj = {**games_data_dict.get(game['name'], {}), **game}

            games_data_dict[game['name']] = game_obj


        self.games_data = list(games_data_dict.values())

        return self.games_data

    def get_games_data(self):
        return self.games_data or self.read_games_data()

    def generate_one_game_xml(self, game_file, game_data, image=None, video=None, manual=None):
        game_xml = ''
        game_xml += "<game>"

        directory_for_game = f"./{self.games_dir}" if self.games_dir is not '.' else self.games_dir

        game_xml += f"<path>{UNIX_PATH.join([directory_for_game, game_file])}</path>"

        if game_data.get('name'):
            game_xml += f"<name>{game_data.get('name')}</name>"
        if game_data.get('description'):
            game_xml += f"<desc>{game_data.get('description')}</desc>"

        if game_data.get('marquee'):
            game_xml += f"<marquee>{game_data.get('marquee')}</marquee>"

        if game_data.get('thumbnail'):
            game_xml += f"<thumbnail>{game_data.get('thumbnail')}</thumbnail>"

        if game_data.get('fanart'):
            game_xml += f"<fanart>{game_data.get('fanart')}</fanart>"

        if game_data.get('map'):
            game_xml += f"<map>{game_data.get('map')}</map>"

        if game_data.get('releasedate'):
            game_xml += f"<releasedate>{game_data.get('releasedate')}</releasedate>"

        if game_data.get('developer'):
            game_xml += f"<developer>{game_data.get('developer')}</developer>"

        if game_data.get('publisher'):
            game_xml += f"<publisher>{game_data.get('publisher')}</publisher>"

        if game_data.get('family'):
            game_xml += f"<family>{game_data.get('family')}</family>"

        if game_data.get('favorite'):
            game_xml += f"<favorite>{game_data.get('favorite')}</favorite>"

        if game_data.get('playcount'):
            game_xml += f"<playcount>{game_data.get('playcount')}</playcount>"

        if game_data.get('lastplayed'):
            game_xml += f"<lastplayed>{game_data.get('lastplayed')}</lastplayed>"

        if game_data.get('md5'):
            game_xml += f"<md5>{game_data.get('md5')}</md5>"

        if game_data.get('lang'):
            game_xml += f"<lang>{game_data.get('lang')}</lang>"

        if image:
            game_xml += f"<image>{image}</image>"
        if video:
            game_xml += f"<video>{video}</video>"
        if manual:
            game_xml += f"<manual>{manual}</manual>"
        if game_data.get('rate'):
            r0 = float(game_data.get('rate').split('/')[0])
            r1 = float(game_data.get('rate').split('/')[1])
            game_xml += f"<rating>{round(r0/r1, 2)}</rating>"
        if game_data.get('genres'):
            game_xml += f"<genre>{', '.join(game_data.get('genres'))}</genre>"
        if game_data.get('players'):
            game_xml += f"<players>{game_data.get('players')}</players>"
        
        game_xml += f"<lang>{self.games_lang}</lang>"

        game_xml += "</game>"

        return game_xml

    def generate_games_xml(self, write=False):
        xml_string = ''
        xml_string += "<gameList>"

        game_files = self.games_files or self.read_games_files()

        for game in game_files:
            game_name = re.sub(self.game_types, '', game)
            image = self.find_image_file_name(game_name)
            manual = self.find_manual_file_name(game_name)
            video = self.find_video_file_name(game_name)
            game_data = self.find_game_data(game_name)

            image_path = image and UNIX_PATH.join(['.', self.images_dir, image])
            manual_path = manual and UNIX_PATH.join(['.', self.manuals_dir, manual])
            video_path = video and UNIX_PATH.join(['.', self.videos_dir, video])

            one_game_xml = self.generate_one_game_xml(game, game_data, image_path, video_path, manual_path)

            xml_string += one_game_xml or ''

        xml_string += "</gameList>"

        self.gamelist_str = xml_string

        write and self.write_gamelist_xml()

        return self.gamelist_str

GAME_TYPES = r"(.gen|.bin|.md|.sg|.smd|.zip|.7z)$"
IMAGE_TYPES = r"(.png|.jpg|.jpeg|.tiff|.gif)$"
VIDEO_TYPES = r"(.mp4|.avi)$"
MANUAL_TYPES = r"(.pdf)$"

def init():
    pass

def main():
    init()

    glp = GamesListProcessor(SETTINGS_PATH, SYSTEM)

    glp.generate_games_xml(True)

if __name__ == '__main__':
    main()
else:
    print("[WARNING] rg351_media not a module!")