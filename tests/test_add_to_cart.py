import pytest
from pages.start_page import StartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@pytest.mark.usefixtures("init_driver", "base_url")
class TestAddToCart:

    def test_add_product_to_cart(self, base_url):
        # Инициализация страницы
        start_page = StartPage(self.driver)

        # Открытие стартовой страницы
        start_page.open_start_page(base_url)

        # ID продукта, который хотим добавить в корзину
        product_id = '253354830'

        # Добавление продукта в корзину
        start_page.add_product_to_cart(product_id)

        # Проверка, что товар добавлен в корзину
        assert start_page.is_product_added_to_cart(), "Product was not added to cart"

    def test_add_several_product_to_cart(self, base_url):
        # Инициализация страницы
        start_page = StartPage(self.driver)

        # Открытие стартовой страницы
        start_page.open_start_page(base_url)

        # ID продукта, который хотим добавить в корзину
        product_id_trapeze = '253354830'
        product_id_rhombus = '253355137'


        # Добавление продукта в корзину
        start_page.add_product_to_cart(product_id_trapeze)
        start_page.add_product_to_cart(product_id_rhombus)

        # Проверка, что товар добавлен в корзину
        assert start_page.is_product_added_to_cart(), "Product was not added to cart"

    @pytest.mark.parametrize("base_url", ["https://demo.yookassa.ru/"])
    def test_is_micro_alert_displayed(self, base_url):
        # Инициализация страницы
        start_page = StartPage(self.driver)
        # Открытие стартовой страницы
        start_page.open_start_page(base_url)
        # ID продукта, который хотим добавить в корзину
        product_id = '253354771'
        # Добавление продукта в корзину
        start_page.add_product_to_cart(product_id)

        # Попытка найти и проверить микро-уведомление
        try :
            micro_alert = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".micro-alert-item.is-success-notice"))
            )
            assert "Товар добавлен в корзину" in micro_alert.text
        except TimeoutException :
            assert False, "Микро-уведомление не отображается"



