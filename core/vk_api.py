import asyncio
from httpx import AsyncClient
from typing import List
import random


class VK:
    def __init__(self, token: str):
        self.client = AsyncClient()
        self.token = f"access_token={token}"
        self.base_url = "https://api.vk.com/"
        self.cities = [
            "Севастополь",
            "Симферополь",
            "Керчь",
            "Евпатория",
            "Ялта",
            "Феодосия",
            "Джанкой",
            "Алушта",
            "Бахчисарай",
            "Саки",
            "Красноперекопск",
            "Армянск",
            "Судак",
            "Белогорск",
            "Инкерман",
            "Щёлкино",
            "Старый Крым",
            "Алупка"
        ]


    def pause(f):

        async def tmp(*args, **kwargs):

            await asyncio.sleep(0.334)
            return await f(*args, **kwargs)
        
        return tmp

    @pause
    async def get_city_id(self, city: str)-> int or None:
        print(city)
        url = self.base_url + f"method/database.getCities?{self.token}&q={city}&v=5.131"

        try:
            response = await self.client.post(url)
            city = response.json()['response']['items'][0]
            print("Город -", city['title'],"\nid -", city['id'])
            return city['id']
        except Exception as ex:
            print("ERROR |get_id_city| -", ex)
            return None

    @pause
    async def get_schools(self, city_id: int, school_name: str=None)-> List[dict] or None:

        url = self.base_url + f"method/database.getSchools?{self.token}&city_id={city_id}&v=5.131"

        try:
            response = await self.client.post(url)
            return response.json()['response']['items']
        except Exception as ex:
            print("ERROR |get_id_school| -", ex)
            return None

    # async def get_id_cities(self):
        

    #     url = self.base_url + f"method/users.get?{self.token}&user_ids=denis_macintosh&v=5.131"

    #     try:
    #         response = await self.client.post(url)
    #         print(response.json())
    #     except Exception as ex:
    #         print(ex)


    # async def get_user(self):
    #     url = self.base_url + f"method/users.get?{self.token}&user_ids=denis_macintosh&v=5.131"

    #     try:
    #         response = await self.client.post(url)
    #         print(response.json())
    #     except Exception as ex:
    #         print(ex)

    @pause
    async def search(self,school_city_id: int, school_id: int, school_year: int)-> List[dict] or None:
        print(school_id)
        url = self.base_url + f"method/users.search?{self.token}&count=1000&school_city={school_city_id}&school={school_id}&school_year={school_year}&v=5.131"

        try:
            response = await self.client.post(url)
            return response.json()['response']['items']
        except Exception as ex:
            print("ERROR |search| -", ex)
            return None


    async def parse_users(self, year: int)-> List[dict]:

        data: List[dict] = []

        
        for city_name in self.cities:
            
            city_id = await self.get_city_id(city_name)
            match (city_id):

                case (None):
                    pass

                case (_):
                    schools = await self.get_schools(city_id)
                    match (schools):

                        case (None):
                            pass

                        case (_):
                            for school in schools:

                                users = await self.search(city_id, school['id'], 2023)
                                match (users):

                                    case (None):
                                        pass

                                    case (_):
                                        for user in users:

                                            data.append({
                                                "link": f"https://vk.com/id{user['id']}",
                                                "first_name": user['first_name'],
                                                "last_name": user['last_name'],
                                                "city": city_name,
                                                "school": school['title'],
                                                "year_to_school": 2023
                                            })
        return data


from dotenv import load_dotenv
load_dotenv()
import os
vk = VK(os.getenv('token_vk'))