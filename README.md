# Web Tours QA Automation Suite (Playwright & Jenkins)

Suite de tests automatisés de bout en bout (E2E) pour l'application de réservation de billets d'avion **Web Tours**.
Ce projet fait suite à la **Partie 1** (gestion de projet sous JIRA et référentiel de tests sous Xray).

---

## 🚀 Technologies utilisées
- **Langage :** Python 3.13
- **Framework de test :** Pytest (v9.2.0)
- **Moteur d'automatisation :** Microsoft Playwright (alternative moderne à Selenium)
- **Rapports de test :** 
  - Rapport interactif HTML (`pytest-html`)
  - Rapport standard XML JUnit (`results.xml` pour Jenkins)
- **CI/CD :** Pipeline déclaratif Jenkins (`Jenkinsfile`)

---

## 📋 Périmètre des Tests Automatisés (5 scénarios ciblés)
1. **`test_01_login_success` (FT) :** Authentification réussie avec vérification de l'accès aux menus membres.
2. **`test_02_login_bad_password` (ET) :** Tentative de connexion avec un mot de passe erroné et contrôle de l'apparition de l'écran d'erreur.
3. **`test_03_flight_search` (FT) :** Recherche de vols disponibles (sélection villes départ/arrivée, dates, passagers) et contrôle des résultats.
4. **`test_04_flight_booking_e2e` (FT / E2E) :** Réservation complète d'un vol avec formulaire de paiement et génération de facture (`Invoice`).
5. **`test_05_sign_off` (FT) :** Déconnexion de l'utilisateur et validation du retour à la mire d'accueil.

---

## 🛠️ Installation & Exécution locale

```bash
# 1. Cloner le projet
git clone https://github.com/ZeinebMkaouar/webtours-qa-automation.git
cd webtours-qa-automation

# 2. Installer les dépendances
pip install -r requirements.txt
playwright install chromium

# 3. Lancer la suite de tests avec génération des rapports
pytest test_webtours.py -v --html=reports/report.html --self-contained-html --junitxml=reports/results.xml
```

---

## 📊 Résultats des Tests
- **Nombre de tests exécutés :** 5
- **Tests réussis :** 5 (100% Passed)
- **Temps total d'exécution :** ~46s

---

## ⚙️ Intégration Continue avec Jenkins
Le projet contient un `Jenkinsfile` prêt pour l'exécution automatique :
1. **Checkout :** Récupération du code source depuis GitHub.
2. **Install Dependencies :** Installation de Python, Playwright et Chromium.
3. **Execute Playwright Tests :** Lancement des 5 tests en mode headless.
4. **Publish Reports :** Publication automatique du graphique des résultats JUnit et du rapport HTML.
