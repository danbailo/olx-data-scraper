from bs4 import BeautifulSoup
import requests
import json
import re
import time
from tqdm import tqdm

headers = {
    'authority': 'www.olx.com.br',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'sec-fetch-dest': 'document',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept-language': 'en,en-US;q=0.9,pt-BR;q=0.8,pt;q=0.7,es;q=0.6',
    'cookie': 'r_id=c6409236-a98c-4384-a301-c3cdba8b7f5d; nl_id=ddaaebb7-2e60-4265-af3a-a594ec76d7a4; _gcl_au=1.1.2095735624.1582570825; _ga=GA1.3.530330864.1582570825; _gid=GA1.3.1312093051.1582570825; l_id=74cf6905-6c6f-4a13-8153-1b009ca922e6; _hjid=ab025417-893b-4f58-be2d-d682e2743fb9; tt.u=0100007F4A1D545E8C06D857024F670D; _sim_uuid=4F2C7FBE-6482-4778-B1CC-0365676BC838; xtvrn=$483760$; xtan=-; xtant=1; TestAB_PUB612=ORIGINAL; TestAB_categorieshome5=ORIGINAL; las=714910315; _ttdmp=E:4|LS:|CA:CA17955,CA17955; TestAB_Groups=advAfshNativo_A.advVideoListing_A.ast-showphone-flow_new.autos-completion-popup_fullFeedback.bj-friendly-redirect_a.bj-HelpMeDecide_SellerOnlineTitle.bj-listItemOpenInANewTab_A.bj-new-listing-desktop-partial_lazy-load-online-sellers.fixedBar2_box.helpcenter-form-v2_control.imo-597-preview_show.imo-749-use-feeds-scheduled-listtime_active.mes-warning-message_new.mfg-autos-market-place-selected-options_early.mfg-autos-market-place_control.myads-new-expired_A.myads-new-pendingpay_A.myads-new-pendingpublish_A.myads-new-published_A.new-checkout-loading_control.osp-flex-plan-cars-subscription_control.osp-flex-plan-realestate-subscription_dropdown.osp-insidesales-phone-web_withphone.osp-new-layout-ai-web_scroll.osp-step-choice-cars-subscription-web_control.osp-step-choice-real-estate-web_control.passwordless-sign-in-on-login_control.passwordless-sign-in-on-register_yes.payments-boletoProgressButton_A.remember-last-login-on-home_control.removalAdOnboard_A.smart-lock-login_control.upr-cards-infinite-scroll_A.upr-chat-adview-profilelink_A.upr-chat-listing-profilelink_A.upr-profile-cards_A.upr-profile-new-account-validation-icons_A.upr-profile-trust-profile-links_A.uprNewMiniProfile_control.uprNewMonthActivityRule_control; _sim_si=94B5B9F1-D94C-4A85-8974-BE24F824BA2A; sq=q=soja&rlt=3&st=a&w=3&cg=1100&f=a; tt_c_vmt=1582658106; tt_c_c=direct; tt_c_s=direct; tt_c_m=direct; tt.nprf=; s_id=949a1f4f-3f5b-453a-a7a7-8522495d12432020-02-25T19:15:06.535Z; _ttuu.s=1582658789355; _sim_li=ZGI2OWQ3ZWItM2ViYi00YjM0LTgwZTAtNjM0ZmRmMTQ2ODdlLmxvY2FsLDQ1LjE3Mi42Ni41OA==; _dc_gtm_UA-70177409-2=1',
}

class Olx:
    def __init__(self):
        self.__base_url = "https://www.olx.com.br"
        self.pages_pattern = re.compile(r"(.*\?o=)(\d+)(.*)")

    def get_urn(self, input_file): #pega as extensoes do txt
        file = open(input_file, "r")
        all_urn = [urn.replace("\n", "") for urn in file.readlines()]
        file.close()
        return all_urn

    def get_pages(self, all_urn): #a partir das extensoes do txt, pega da page 1 ate a ultima
        all_pages = []
        for urn in all_urn:
            uri = self.__base_url + urn
            response = requests.get(uri, headers=headers)
            if not response.ok:
                print("Request error!")
                return False
            soup = BeautifulSoup(response.text, "html.parser")
            last_page_link = soup.find("a", attrs={"title": "Última página"}).get("href")
            first, last_page, second = self.pages_pattern.match(last_page_link).groups()
            pages = [first + str(i) + second for i in range(1, int(last_page) + 1)]
            all_pages.extend(pages)
        return all_pages

    def get_links(self, pages): #coleta os links de cada anuncio de todas as paginas
        links = []
        request_error = 0
        while True:
            try:
                response = requests.get(pages, headers=headers)
                if not response.ok:
                    print("Request error!")
                    return False
                soup = BeautifulSoup(response.text, "html.parser")
                ul = soup.find("ul", attrs={"id": "main-ad-list"})
                for link in ul.find_all("a"):
                    links.append(link.get("href"))
                break
            except Exception as err:
                print(err)
                request_error += 1
                if request_error >= 10:
                    print("Request error, tries exceeded!")
                    return False
        return links

    def get_json(self, links):
        request_error = 0
        while True:
            try:
                response = requests.get(links, headers=headers)
                break
            except Exception:
                print("Sleeping... 1sec")
                time.sleep(1)
                request_error += 1
                if request_error >= 10:
                    print("Request error, tries exceeded!")
                    return False
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            script_tag = soup.find("script", attrs={"data-json":re.compile(".*")}).get("data-json")
        except AttributeError:
            print("error")
            return self.get_json(links)
        json_data = json.loads(script_tag)

        id_announcement = json_data["ad"]["listId"]

        municipality = json_data["ad"]["location"]["municipality"]
        state = json_data["ad"]["location"]["uf"]
        zipcode = json_data["ad"]["location"]["zipcode"]
        price = json_data["ad"]["priceValue"]

        lenght = ""
        for len_properties in json_data["ad"]["properties"]:
            if len_properties["label"] == "Tamanho":
                lenght = len_properties["value"]

        type_ = ""
        for type_properties in json_data["ad"]["properties"]:
            if type_properties["label"] == "Tipo":
                type_ = type_properties["value"]   

        title = json_data["ad"]["subject"]         
        description = json_data["ad"]["description"]
        try:
            imgs = [img["original"] for img in json_data["ad"]["images"]]
        except KeyError:
            imgs = []
        phone = json_data["ad"]["phone"]["phone"]
        ddd = json_data["ad"]["location"]["ddd"]
        url = json_data["ad"]["friendlyUrl"]
        date_hour = json_data["ad"]["listTime"]
        professional = json_data["ad"]["professionalAd"]      

        return (
            id_announcement,
            municipality,
            state,
            zipcode,
            price,
            lenght,
            type_,
            title,
            description,
            imgs,
            ddd,
            phone,
            url,
            date_hour,
            professional,
        )


