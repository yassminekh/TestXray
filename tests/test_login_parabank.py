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
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    driver.implicitly_wait(15)
    return driver


class TestParaBankLogin(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.wait   = WebDriverWait(self.driver, 30)  # augmenté à 30s
        self.driver.get(BASE_URL)

    def tearDown(self):
        self.driver.quit()

    def test_TX_91_login_valide(self):
        """TX-91 — Vérifier la page login avec identifiants valides"""

        # ── Étape 1 : Remplir username ────────────────────────────────────────
        username_field = self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.clear()
        username_field.send_keys(VALID_USER)

        # ── Étape 2 : Remplir password ────────────────────────────────────────
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.clear()
        password_field.send_keys(VALID_PASS)

        # ── Étape 3 : Cliquer sur Login ───────────────────────────────────────
        self.driver.find_element(
            By.CSS_SELECTOR, "input.button[type='submit']"
        ).click()

        # ── Étape 4 : Attendre le changement d'URL (overview ou login.htm) ────
        self.wait.until(
            EC.any_of(
                EC.url_contains("overview"),
                EC.url_contains("activity"),
                EC.presence_of_element_located((By.ID, "accountTable")),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error"))
            )
        )

        # ── Étape 5 : Vérifier qu'on n'est PAS sur une page d'erreur ──────────
        current_url = self.driver.current_url
        print(f"\nURL après login : {current_url}")
        print(f"Titre page      : {self.driver.title}")

        # Vérifier absence d'erreur
        error_elements = self.driver.find_elements(By.CSS_SELECTOR, ".error")
        if error_elements:
            error_text = error_elements[0].text
            self.fail(f"Erreur de login affichée : {error_text}")

        # ── Étape 6 : Vérifier que le login est réussi ────────────────────────
        self.assertTrue(
            "overview" in current_url or
            "activity" in current_url or
            self.driver.find_elements(By.ID, "accountTable"),
            f"Login échoué. URL actuelle : {current_url}"
        )

        print("✅ Login réussi !")


if __name__ == "__main__":
    unittest.main()