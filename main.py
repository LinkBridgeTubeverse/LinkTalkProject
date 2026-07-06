import os

def get_affiliate_link(product_url: str) -> str:
    affiliate_id = os.environ["AFFILIATE_ID"]  # GitHub Secrets에 등록한 값 (_c4owRCtR)
    return f"https://s.click.aliexpress.com/e/{affiliate_id}?target={product_url}"

if __name__ == "__main__":
    product_url = "https://ko.aliexpress.com/item/1005010661950273.html"
    affiliate_link = get_affiliate_link(product_url)
    print("생성된 제휴 링크:", affiliate_link)
