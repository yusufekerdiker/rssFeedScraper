# import requests
# import json
# import xmltodict

# result = requests.get("https://www.technopat.net/feed")
# with open(result) as xml_file:
#     data_dict = xmltodict.parse(xml_file.read())
#     json_data = json.dumps(data_dict)
# # result = result.text
# json_data = json.loads(json_data.text)

# # print(type(result))
# # print(result)
# print(json_data[0]["title"])

from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.technopat.net/feed")
# print(url)
soup = BeautifulSoup(url.content, "xml")

#find all news which is inside item tag
items = soup.find_all("item")

for item in items:
# loop in the news and get details of it
    title = item.title.text
    link = item.link.text
    creator = item.creator.text
    publishDate = item.pubDate.text

    # technopat halihazırda kelime temelli kategorileme yapıyor
    # buna ulaşmak için her bir haberin yani item',in
    # içinde gezip o kategorileri bir arrey'e atıyorum
    # soup.findall dersek sayfadaki tüm kategorileri çekiyor, sonradan farkettiğim bir hata :)
    category_elements = item.find_all("category")
    category_names = []
    for category_element in category_elements:
        category_names.append(category_element.text)

    # for category_item in categories:
    #     category = category_item.category.text
    # categories = item.category.text

    #content = item.description.find('p').text
    # technopat haberin açıklamasını descriptionun içindeki ilk p tagında yazıyor, && yerine and ! yerine not
    # Recursive = False returns only the children of the element of the tag you are trying to find. 
    # https://stackoverflow.com/a/69891061
    #content = item.description.find(lambda tag: tag.name == 'p' and not tag.find('img', recursive=False)).text

    # if item.find("description") is not None and item.find("description").text.strip():
    #     first_p_tag = item.find("p")
    #     content = first_p_tag.text if first_p_tag is not None else ""
    # else:
    #     content = ""

    description = item.description.text
    # yukarıdaki bs de işlemi xml olarak yapıyordum ama burada açıklamanın içi 
    # html olduğu için yeni bs tipine geçtim yani html okuma
    desc_soup = BeautifulSoup(description, "html.parser")
    first_p = desc_soup.find("p") # yukarıda da dediğim gibi haber açıklaması ilk p de olduğu için sadece find ile buldum

    # eğer first p varsa onun textini yani içindeki metini yeni bir değer ata
    # eğer yoksa değeri boş olarak göster
    if first_p:
        first_p_content = first_p.text
    else:
        first_p_content = ""

    articleImage = item.thumbnail['url']

    print(f"Title:{title}\n\nLink:{link}\n\nCreator:{creator}\n\nPublish Date:{publishDate}\n\nCategories:{category_names}\n\nDescription:{first_p_content}\n\nImage:{articleImage}\n\n----------------------------------\n\n")
