import os
import random

def get_affiliate_link(product_url: str) -> str:
    affiliate_id = os.environ["AFFILIATE_ID"]  # GitHub Secrets에 등록한 값 (_c4owRCtR)
    return f"https://s.click.aliexpress.com/e/{affiliate_id}?target={product_url}"

if __name__ == "__main__":
    # 여러 상품 URL을 리스트로 준비
    products = [
        "https://ko.aliexpress.com/item/1005010661950273.html",
        "https://ko.aliexpress.com/item/987654321.html",
        "https://ko.aliexpress.com/item/123456789.html"
    ]

    # 실행할 때마다 랜덤으로 하나 선택
    product_url = random.choice(products)
    affiliate_link = get_affiliate_link(product_url)

    print("랜덤으로 선택된 제휴 링크:", affiliate_link)
