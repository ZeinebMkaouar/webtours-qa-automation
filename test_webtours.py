import pytest

def get_frames(page):
    """Récupère les frames 'navbar' et 'info' de Web Tours avec attente."""
    page.wait_for_timeout(1000)
    navbar = page.frame(name="navbar")
    info = page.frame(name="info")
    return navbar, info

def test_01_login_success(page):
    """FT-01 : Connexion réussie avec des identifiants valides."""
    navbar, info = get_frames(page)
    assert navbar is not None, "Frame 'navbar' non trouvée"
    
    # Saisie des identifiants
    navbar.fill("input[name='username']", "jojo")
    navbar.fill("input[name='password']", "bean")
    navbar.click("input[name='login']")
    
    # Attente de chargement de la session
    page.wait_for_timeout(1500)
    navbar, info = get_frames(page)
    
    # Vérification : Les boutons de navigation doivent être visibles
    assert navbar.locator("img[alt='Search Flights Button']").is_visible(), "Le bouton 'Search Flights' devrait être visible"
    assert navbar.locator("img[alt='SignOff Button']").is_visible(), "Le bouton 'SignOff' devrait être visible"
    
    # Vérification : Message de bienvenue dans la frame info
    info_text = info.content()
    assert "Welcome, <b>jojo</b>" in info_text or "Welcome" in info_text, "Message de bienvenue attendu"

def test_02_login_bad_password(page):
    """ET-02 : Connexion échouée avec mot de passe incorrect."""
    navbar, info = get_frames(page)
    assert navbar is not None
    
    navbar.fill("input[name='username']", "jojo")
    navbar.fill("input[name='password']", "wrong_password_123")
    navbar.click("input[name='login']")
    
    page.wait_for_timeout(1500)
    _, info = get_frames(page)
    
    info_text = info.content()
    assert "Web Tours Error" in info_text or "Bad Password" in info_text, "L'écran d'erreur 'Bad Password' devrait s'afficher"

def test_03_flight_search(page):
    """FT-03 : Recherche de vol entre deux villes."""
    navbar, _ = get_frames(page)
    navbar.fill("input[name='username']", "jojo")
    navbar.fill("input[name='password']", "bean")
    navbar.click("input[name='login']")
    page.wait_for_timeout(1500)
    
    # Clic sur le bouton Search Flights
    navbar, _ = get_frames(page)
    navbar.click("img[alt='Search Flights Button']")
    page.wait_for_timeout(1500)
    
    _, info = get_frames(page)
    # Sélection des villes de départ et d'arrivée
    info.select_option("select[name='depart']", "Denver")
    info.select_option("select[name='arrive']", "London")
    info.fill("input[name='numPassengers']", "1")
    
    # Clic sur Continue (recherche de vols)
    info.click("input[name='findFlights']")
    page.wait_for_timeout(1500)
    
    _, info = get_frames(page)
    info_text = info.content()
    # Vérification que la liste des vols proposés est affichée
    assert "Flight departing from" in info_text or "Select Flight" in info_text or "Denver to London" in info_text, "La liste des vols devrait être affichée"

def test_04_flight_booking_e2e(page):
    """FT-04 : Réservation complète d'un vol de bout en bout avec facture (Invoice)."""
    navbar, _ = get_frames(page)
    navbar.fill("input[name='username']", "jojo")
    navbar.fill("input[name='password']", "bean")
    navbar.click("input[name='login']")
    page.wait_for_timeout(1500)
    
    # Accès à la recherche de vol
    navbar, _ = get_frames(page)
    navbar.click("img[alt='Search Flights Button']")
    page.wait_for_timeout(1500)
    
    # Choix départ/arrivée et recherche
    _, info = get_frames(page)
    info.select_option("select[name='depart']", "Denver")
    info.select_option("select[name='arrive']", "London")
    info.click("input[name='findFlights']")
    page.wait_for_timeout(1500)
    
    # Sélection du vol proposé
    _, info = get_frames(page)
    info.click("input[name='reserveFlights']")
    page.wait_for_timeout(1500)
    
    # Remplissage des informations de paiement
    _, info = get_frames(page)
    info.fill("input[name='creditCard']", "1234567890123456")
    info.fill("input[name='expDate']", "12/28")
    info.click("input[name='buyFlights']")
    page.wait_for_timeout(1500)
    
    # Vérification de l'émission de la facture (Invoice)
    _, info = get_frames(page)
    invoice_content = info.content()
    assert "Invoice" in invoice_content or "Reservation Made" in invoice_content or "Thank you for booking" in invoice_content, "La facture Invoice devrait être affichée"

def test_05_sign_off(page):
    """FT-05 : Déconnexion de l'utilisateur et fin de session."""
    navbar, _ = get_frames(page)
    navbar.fill("input[name='username']", "jojo")
    navbar.fill("input[name='password']", "bean")
    navbar.click("input[name='login']")
    page.wait_for_timeout(1500)
    
    # Clic sur le bouton SignOff
    navbar, _ = get_frames(page)
    navbar.click("img[alt='SignOff Button']")
    page.wait_for_timeout(1500)
    
    # Vérification que le formulaire de login est réaffiché
    navbar, _ = get_frames(page)
    assert navbar.locator("input[name='username']").is_visible(), "L'écran de connexion initial devrait être réaffiché après SignOff"
