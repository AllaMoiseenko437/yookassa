from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException


class StartPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Локатор для поиска товара по data-product-id
    def product_form_locator(self, product_id):
        return By.XPATH, f'//form[@data-product-id="{product_id}"]'

    # Локатор для кнопки "В корзину" внутри формы продукта
    def add_to_cart_button_locator(self, product_id):
        return (
            By.XPATH, f'//form[@data-product-id="{product_id}"]//button[contains(@class, "product-preview__buy-btn")]')

    # Локатор для проверки успешного добавления в корзину (пример, может отличаться)
    def cart_success_locator(self):
        return By.XPATH, '//div[contains(@class, "micro-alert-item")]'

    # Метод для добавления продукта в корзину
    def add_product_to_cart(self, product_id):
        # Найти форму продукта
        product_form = self.find_element(self.product_form_locator(product_id))

        # Навести на кнопку "В корзину"
        self.hover(self.add_to_cart_button_locator(product_id))

        # Кликнуть по кнопке "В корзину"
        self.click(self.add_to_cart_button_locator(product_id))

    # Метод для открытия главной страницы (или другой нужной страницы)
    def open_start_page(self, base_url):
        #self.open_page()
        self.driver.get(base_url)

    # Метод для проверки, что товар добавлен в корзину
    #def is_product_added_to_cart(self):
     #   return self.find_element(self.cart_success_locator())

    def is_product_added_to_cart(self):
        return len(self.find_elements(self.cart_success_locator())) > 0

    def get_cart_items(self):
        # Код для извлечения элементов из корзины
        cart_items = []

        cart_items_elements = self.driver.find_elements(By.CLASS_NAME, 'cart-item')

        for item in cart_items_elements:
            product_id = item.get_attribute(
                'data-product-id')  # Или используйте любой другой способ получения ID продукта
            cart_items.append({'product_id': product_id})

        return cart_items



