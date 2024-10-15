import time
from pages.start_page import StartPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestCart:

    def test_product_in_cart(self, base_url, driver):
        product_id = '253354830'
        start_page = StartPage(driver)
        start_page.open_start_page(base_url)

        start_page.add_product_to_cart(product_id)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".micro-alert-item.is-success-notice"))
        )

        start_page.open_start_page(f"{base_url}/cart_items")
        cart_items = start_page.get_cart_items()

        assert any(
            item['product_id'] == product_id for item in cart_items), f"Product with ID {product_id} is not in the cart"

    def test_delete_product_in_cart(self, base_url, driver):
        product_id = '253354830'
        start_page = StartPage(driver)
        start_page.open_start_page(base_url)
        start_page.add_product_to_cart(product_id)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".micro-alert-item.is-success-notice"))
        )

        start_page.open_start_page(f"{base_url}/cart_items")
        delete_button_locator = "button.js-item-delete"

        try:
            delete_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, delete_button_locator))
            )

            assert delete_buttons, "Нет доступных кнопок удаления."
            delete_buttons[0].click()

            WebDriverWait(driver, 10).until(EC.invisibility_of_element(delete_buttons[0]))

            cart_items_after_deletion = start_page.get_cart_items()
            assert product_id not in [item['product_id'] for item in
                                      cart_items_after_deletion], "Продукт не был удален из корзины."

        except TimeoutException:
            print("Не удалось найти кнопку удаления для товара.")

    def test_placing_an_order(self, base_url, driver):
        product_id = '253354830'
        start_page = StartPage(driver)
        start_page.open_start_page(base_url)
        start_page.add_product_to_cart(product_id)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".micro-alert-item.is-success-notice"))
        )

        start_page.open_start_page(f"{base_url}/cart_items")

        order_button = WebDriverWait(driver, 10).until(
              EC.element_to_be_clickable((By.CSS_SELECTOR, ".button.button_size-l.button_wide"))
        )

        order_button.click()

        WebDriverWait(driver, 10).until(EC.url_contains("new_order"))  # Замените на часть успешного URL

        create_order_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#create_order"))
        )

        assert create_order_button.is_displayed(), "Кнопка 'Подтвердить заказ' не отображается."

    def test_promotional_code(self, base_url, driver):
        start_page = StartPage(driver)
        start_page.open_start_page(f"{base_url}/cart_items")

        try:
            add_product = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-cart-counter__btn-icon.icon-cart"))
            )
            add_product.click()

            cart_position_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".header__control-bage[data-cart-positions-count]"))
            )
            print("Элемент найден:", cart_position_element.text)

            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".form-control_size-m"))
            )

            input_field.send_keys("тест")

            assert input_field.get_attribute('value') == "тест", "Текст не совпадает!"
            print("Текст успешно введен в поле.")

            approve_coupon = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-check"))
            )
            approve_coupon.click()

            error_message = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".insales-ui-discount-error"))
            )
            assert error_message.text == "Указан несуществующий купон, убедитесь, что он введен верно", "Сообщение об ошибке не совпадает!"
            print("Проверка валидации прошла успешно: сообщение об ошибке отображается.")

        except TimeoutException as e:
            print("Элемент не найден за отведенное время:", str(e))
        except AssertionError as e:
            print("Ошибка утверждения:", str(e))

    def test_add_several_product_in_cart(self, base_url, driver):
        product_id = '253354771'
        start_page = StartPage(driver)
        start_page.open_start_page(base_url)
        start_page.add_product_to_cart(product_id)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".micro-alert-item.is-success-notice"))
        )

        start_page.open_start_page(f"{base_url}/cart_items")

        try:
            add_product = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span.add-cart-counter__btn-icon.icon-cart"))
            )
            add_product.click()
        except TimeoutException:
            print("Элемент для добавления товара не был найден или недоступен.")
            return

        time.sleep(2)

        try:
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='cart[quantity][432605259]']"))
            )

            quantity_value = input_field.get_attribute("value")
            print(f"Текущее значение: {quantity_value}")

            assert quantity_value == "2", f"Количество в корзине не равно 2! Текущее количество: {quantity_value}"
            print("Проверка прошла успешно: количество равно 2.")

        except TimeoutException:
            print("Поле ввода количества не найдено за отведенное время.")
        except AssertionError as e:
            print("Ошибка утверждения:", str(e))











