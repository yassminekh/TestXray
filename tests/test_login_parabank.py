import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL   = "https://parabank.parasoft.com/parabank/index.htm"
VALID_USER = "Bennani@!"
VALID_PASS = "asma@bennani!!!2024"


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(10)
    return driver


class TestParaBankLogin(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.wait   = WebDriverWait(self.driver, 15)
        self.driver.get(BASE_URL)

    def tearDown(self):
        self.driver.quit()

    def test_TX_91_login_valide(self):
        """TX-91 — Vérifier la page login avec identifiants valides"""

        # ── Étape 1 : Remplir le champ username ──────────────────────────────
        username_field = self.driver.find_element(By.NAME, "username")
        username_field.clear()
        username_field.send_keys(VALID_USER)

        # ── Étape 2 : Remplir le champ password ──────────────────────────────
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(VALID_PASS)

        # ── Étape 3 : Cliquer sur le bouton Login ────────────────────────────
        self.driver.find_element(
            By.CSS_SELECTOR, "input.button[type='submit']"
        ).click()

        # ── Étape 4 : Vérifier la redirection vers /overview ─────────────────
        self.wait.until(EC.url_contains("/overview"))

        self.assertIn(
            "/overview",
            self.driver.current_url,
            f"Après login valide, l'URL doit contenir '/overview'. URL actuelle : {self.driver.current_url}"
        )

        # ── Étape 5 : Vérifier que la page Accounts Overview est affichée ────
        accounts_table = self.wait.until(
            EC.visibility_of_element_located((By.ID, "accountTable"))
        )
        self.assertTrue(
            accounts_table.is_displayed(),
            "La table des comptes doit être visible après connexion"
        )

        # ── Étape 6 : Vérifier que le bouton Log Out est présent ─────────────
        logout_link = self.wait.until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Log Out"))
        )
        self.assertTrue(
            logout_link.is_displayed(),
            "Le bouton Log Out doit être visible après connexion"
        )


if __name__ == "__main__":
    unittest.main()