#For all car makes + post codes MB do yourself manually loggs in perfectly

import time
import csv
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.support.ui import Select


# ---------- CONFIG ----------
BASE_URL = "https://www.carwow.co.uk/used-cars"
POSTCODE = "E1 7DB"
DISTANCE = "50"  # miles
YEAR_FROM = "2013"
YEAR_TO = "2018"
CAR_MAKE = "BMW"
FUEL_TYPE = "Diesel"

# ---------- SETUP ----------
# Don't create driver here - we'll create it in main function
options = None
driver = None
wait = None
actions = None


def safe_click(element):
    driver.execute_script("arguments[0].click();", element)


def load_cookies_if_available():
    """Load cookies for logged-in session if cookie file exists"""
    # Check for cookie files in order of preference
    cookie_file = None
    if os.path.exists("carwow_manual_cookies.json"):
        cookie_file = "carwow_manual_cookies.json"
        print("📌 Found manual cookies file")
    elif os.path.exists("carwow_login_cookies.json"):
        cookie_file = "carwow_login_cookies.json"
        print("📌 Found login cookies file")
    elif os.path.exists("carwow_cookies.json"):
        cookie_file = "carwow_cookies.json"
        print("📌 Found default cookies file")
    
    if not cookie_file:
        print("ℹ️ No cookie file found - proceeding without login")
        return False
    
    try:
        # Load cookies from file
        with open(cookie_file, "r", encoding="utf-8") as f:
            cookies = json.load(f)
        
        # Add cookies to browser
        success = 0
        for cookie in cookies:
            # Remove problematic fields
            cookie.pop("sameSite", None)
            cookie.pop("storeId", None)
            cookie.pop("id", None)
            cookie.pop("hostOnly", None)
            cookie.pop("session", None)
            
            try:
                driver.add_cookie(cookie)
                success += 1
            except Exception as e:
                continue
        
        if success > 0:
            print(f"✅ Loaded {success}/{len(cookies)} cookies")
            # Don't refresh yet - let the page load naturally
            return True
        else:
            print("⚠️ Could not load any cookies")
            return False
            
    except Exception as e:
        print(f"⚠️ Error loading cookies: {e}")
        return False



def set_postcode_and_distance(postcode_value="E1 7DB", distance="50"):
    # First dismiss any popups that might be blocking
    dismiss_popups_and_banners()
    time.sleep(0.3)  # Reduced from 1 second
    
    # Enter postcode with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            postcode = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input#location-desktop[name='postcode']")))
            
            # Scroll to element and ensure it's in view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", postcode)
            time.sleep(0.2)  # Reduced from 0.5 seconds
            
            # Try different methods to interact with the field
            try:
                # Method 1: Direct click
                postcode.click()
            except:
                try:
                    # Method 2: JavaScript click
                    driver.execute_script("arguments[0].click();", postcode)
                except:
                    # Method 3: Actions chain
                    actions.move_to_element(postcode).click().perform()
            
            # Clear and enter new postcode
            postcode.clear()
            driver.execute_script("arguments[0].value = '';", postcode)
            time.sleep(0.2)  # Reduced from 0.5 seconds
            postcode.send_keys(postcode_value)
            
            # If we got here without exception, break the retry loop
            break
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                dismiss_popups_and_banners()
                time.sleep(0.8)  # Reduced from 2 seconds
            else:
                raise e

    # Wait for postcode spinner to hide (with timeout)
    try:
        spinner = driver.find_element(By.CSS_SELECTOR,
            "div[data-stock-cars-v2--location-target='spinner']")
        WebDriverWait(driver, 5).until(lambda d: "stock-cars-v2__postcode-spinner--hidden" in spinner.get_attribute("class"))
    except:
        pass  # Continue if spinner check fails

    # Wait for 'Set location' button to appear in DOM and become clickable
    set_btn = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "input[type='submit'][value='Set location']")))
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input[type='submit'][value='Set location']")))

    driver.execute_script("arguments[0].scrollIntoView(true);", set_btn)
    driver.execute_script("arguments[0].click();", set_btn)  # safer than normal click

    print("✅ Postcode & Distance set")

    # Select distance (after button is clicked, dropdown gets enabled)
    distance_select = Select(wait.until(
        EC.element_to_be_clickable((By.ID, "location-lte-desktop"))))
    distance_select.select_by_value(distance)

    time.sleep(0.3)  # Reduced from 1 second

def set_age_range(year_from=2013, year_to=2018):
    # 1. Expand Age dropdown
    age_label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='age-desktop-expander']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", age_label)
    driver.execute_script("arguments[0].click();", age_label)

    # 2. Wait for selects
    age_from_select = wait.until(EC.presence_of_element_located((By.ID, "age-gte-desktop")))
    age_to_select = wait.until(EC.presence_of_element_located((By.ID, "age-lte-desktop")))

    from_select = Select(age_from_select)
    to_select = Select(age_to_select)

    for option in from_select.options:
        if str(year_from) in option.text:
            from_select.select_by_visible_text(option.text)
            break

    for option in to_select.options:
        if str(year_to) in option.text:
            to_select.select_by_visible_text(option.text)
            break

    print(f"✅ Age range set: {year_from} - {year_to}")
    time.sleep(0.3)  # Reduced from 1 second

def set_make(car_make="BMW"):
    wait = WebDriverWait(driver, 15)  # Increased timeout

    # 1️⃣ Open the "Make" dropdown
    make_label = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "label[for='brand-desktop-expander']"))
    )
    driver.execute_script("arguments[0].click();", make_label)
    print("🔽 Make dropdown opened")

    # 2️⃣ Wait for the search box
    search_box = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input#brand-search"))
    )

    # 3️⃣ Type the make
    search_box.clear()
    
    # For Mercedes-Benz, try typing just "Mercedes" to trigger the suggestion
    if car_make.upper() == "MERCEDES-BENZ":
        search_text = "Mercedes"
    else:
        search_text = car_make
    
    search_box.send_keys(search_text)
    print(f"⌨️ Typed: {search_text}")
    time.sleep(0.8)  # Reduced from 2 seconds - for suggestions to appear

    # 4️⃣ Try multiple strategies to find and click the option
    clicked = False
    
    # Strategy 1: Try to find by partial text match in any element
    try:
        if car_make.upper() == "MERCEDES-BENZ":
            # Look for any clickable element containing "Mercedes"
            options = driver.find_elements(By.XPATH, 
                "//label[contains(@class, 'stock-cars-v2__brand-option')]")
            for option in options:
                if "mercedes" in option.text.lower():
                    driver.execute_script("arguments[0].scrollIntoView(true);", option)
                    time.sleep(0.2)  # Reduced from 0.5 seconds
                    driver.execute_script("arguments[0].click();", option)
                    clicked = True
                    print(f"✅ Clicked Mercedes option using text search")
                    break
    except:
        pass
    
    # Strategy 2: Try original data-value approach if not Mercedes or if Strategy 1 failed
    if not clicked:
        try:
            make_value = car_make.lower().replace("-", "_")  # Try underscore
            option_label = driver.find_element(By.XPATH, f"//label[@data-value='{make_value}']")
            driver.execute_script("arguments[0].click();", option_label)
            clicked = True
            print(f"✅ Make selected using data-value: {make_value}")
        except:
            pass
    
    # Strategy 3: Try without separator
    if not clicked:
        try:
            make_value = car_make.lower().replace("-", "")  # Try no separator
            option_label = driver.find_element(By.XPATH, f"//label[@data-value='{make_value}']")
            driver.execute_script("arguments[0].click();", option_label)
            clicked = True
            print(f"✅ Make selected using data-value: {make_value}")
        except:
            pass
    
    # Strategy 4: Click the first visible option if it's the only one
    if not clicked:
        try:
            time.sleep(0.3)  # Reduced from 1 second
            first_option = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "label.stock-cars-v2__brand-option:not(.stock-cars-v2__brand-option--hidden)")
            ))
            driver.execute_script("arguments[0].click();", first_option)
            clicked = True
            print(f"✅ Clicked first visible option")
        except:
            pass
    
    if not clicked:
        print(f"⚠️ Could not select {car_make}, continuing anyway...")
    else:
        print(f"✅ Make selected: {car_make}")


def set_fuel(fuel_type="Diesel"):
    wait = WebDriverWait(driver, 10)

    # 1️⃣ Open the Fuel dropdown
    fuel_dd = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "label[for='fuel_type-desktop-expander']"))
    )
    driver.execute_script("arguments[0].click();", fuel_dd)
    print("🔽 Fuel dropdown opened")

    # 2️⃣ Wait for the correct fuel option <label> (by its visible text)
    fuel_option_label = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//label[contains(., '{fuel_type}')]"
    )))

    # 3️⃣ Click the label (this will check the hidden checkbox)
    driver.execute_script("arguments[0].click();", fuel_option_label)
    print(f"✅ Fuel type selected: {fuel_type}")

def get_listing_details(url):
    """Open a car listing and extract dealer name and phone number"""
    seller_name = ""
    contact_number = ""
    car_reg = ""
    
    try:
        # Open listing in new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        time.sleep(1.5)  # Reduced from 3 seconds
        
        # Dismiss any popups on the listing page
        dismiss_popups_and_banners()
        
        # Try to get car registration number
        try:
            reg_element = driver.find_element(By.CSS_SELECTOR, "[class*='registration'], [class*='reg-plate'], .vrm")
            car_reg = reg_element.text.strip()
        except:
            pass
        
        # First try to get dealer name from the page before clicking anything
        try:
            # Look for dealer name in various places
            dealer_selectors = [
                ".dealer-info__name",
                ".dealer-name",
                "[class*='dealer-name']",
                ".seller-name",
                ".dealership-name",
                "h2[class*='dealer']",
                ".stock-banner__dealer-name"
            ]
            
            for selector in dealer_selectors:
                try:
                    dealer_elem = driver.find_element(By.CSS_SELECTOR, selector)
                    if dealer_elem.text.strip():
                        seller_name = dealer_elem.text.strip()
                        break
                except:
                    continue
        except:
            pass
        
        # Click "Call now" button to reveal phone number modal
        try:
            # Find and click the Call now button
            call_button = None
            
            # First try the exact selector from the HTML you provided
            try:
                call_button = driver.find_element(By.CSS_SELECTOR, 
                    "label[data-conversion-name='user_clicked_call_button']")
            except:
                # Try other possible selectors
                call_selectors = [
                    "label[for*='contact-dealership-modal']",
                    "button:contains('Call')",
                    ".contact-cta-group__item",
                    "[data-interaction-element*='Call']"
                ]
                
                for selector in call_selectors:
                    try:
                        call_button = driver.find_element(By.CSS_SELECTOR, selector)
                        if call_button:
                            break
                    except:
                        continue
            
            if call_button:
                driver.execute_script("arguments[0].scrollIntoView(true);", call_button)
                time.sleep(0.3)  # Reduced from 1 second
                driver.execute_script("arguments[0].click();", call_button)
                time.sleep(0.8)  # Reduced from 2 seconds - Wait for modal to appear
                
                # Now extract dealer name and phone from the modal
                if not seller_name:  # If we didn't get the name earlier
                    try:
                        # The dealer name appears in the first step description
                        # Format: "Make a note of your Offer ID below, [Dealer Name] will ask you for it:"
                        step_descriptions = driver.find_elements(By.CSS_SELECTOR, 
                            ".dealer-contact__step-description")
                        
                        for desc in step_descriptions:
                            text = desc.text
                            # Look for pattern: "below, [Dealer Name] will ask"
                            if "will ask you for it" in text:
                                # Extract dealer name between "below, " and " will ask"
                                start = text.find("below, ")
                                if start != -1:
                                    start += 7  # length of "below, "
                                    end = text.find(" will ask", start)
                                    if end != -1:
                                        seller_name = text[start:end].strip()
                                        break
                            # Also check for "Call and ask for <strong>Name</strong>" pattern
                            elif "Call and ask for" in text:
                                try:
                                    strong_elem = desc.find_element(By.TAG_NAME, "strong")
                                    if strong_elem:
                                        seller_name = strong_elem.text.strip()
                                        # Remove "Team" suffix if present
                                        seller_name = seller_name.replace(" Team", "")
                                        break
                                except:
                                    pass
                    except Exception as e:
                        print(f"      ⚠️ Could not extract dealer name from modal: {str(e)[:30]}")
                
                # Get the actual dealer phone number (not Carwow's number)
                try:
                    # The actual dealer number is in .dealer-contact__phone-number
                    phone_elem = driver.find_element(By.CSS_SELECTOR, 
                        ".dealer-contact__phone-number")
                    if phone_elem:
                        # Get the visible text (e.g., "0300 131 1280")
                        contact_number = phone_elem.text.strip()
                        
                        # If no visible text, try the href attribute
                        if not contact_number:
                            href = phone_elem.get_attribute("href")
                            if href and "tel:" in href:
                                # Extract just the main number, not the extension
                                tel_number = href.replace("tel:", "").split(",")[0]
                                contact_number = tel_number
                except:
                    # Fallback: look for any phone number in the modal
                    try:
                        phone_links = driver.find_elements(By.CSS_SELECTOR, 
                            ".modal-content a[href^='tel:'], .dealer-contact a[href^='tel:']")
                        for link in phone_links:
                            text = link.text.strip()
                            # Skip Carwow's generic number
                            if text and "+442045722657" not in text and "2045722657" not in text:
                                contact_number = text
                                break
                    except:
                        pass
                        
        except Exception as e:
            print(f"   ⚠️ Could not get phone details: {str(e)[:50]}")
    
    except Exception as e:
        print(f"   ⚠️ Error getting listing details: {str(e)[:50]}")
    
    finally:
        # Close the tab and switch back to main window
        try:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass
    
    return seller_name, contact_number, car_reg


def get_next_page():
    """Check if there's a next page and navigate to it"""
    try:
        # Look for the pagination section
        pagination = driver.find_elements(By.CSS_SELECTOR, ".pagination__page")
        
        # Find the currently active page
        try:
            current_page_elem = driver.find_element(By.CSS_SELECTOR, 
                ".pagination__page--active, .pagination__page.active")
            current_page = int(current_page_elem.text.strip())
        except:
            current_page = 1
        
        # Look for next page link
        next_page = current_page + 1
        next_page_found = False
        
        for page_elem in pagination:
            try:
                # Check if this is a link (has an 'a' tag)
                link = page_elem.find_element(By.TAG_NAME, "a")
                page_num_text = link.text.strip()
                
                # Check if this is the next page number
                if page_num_text.isdigit() and int(page_num_text) == next_page:
                    # Scroll to the pagination element
                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.3)  # Reduced from 1 second
                    
                    # Click the next page link
                    driver.execute_script("arguments[0].click();", link)
                    print(f"   📄 Moving to page {next_page}...")
                    time.sleep(2)  # Reduced from 5 seconds - Wait for new page to load
                    next_page_found = True
                    break
            except:
                continue
        
        # Alternative: Look for "Next" button
        if not next_page_found:
            try:
                next_button = driver.find_element(By.XPATH, 
                    "//a[contains(text(), 'Next')] | //button[contains(text(), 'Next')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(0.3)  # Reduced from 1 second
                driver.execute_script("arguments[0].click();", next_button)
                print(f"   📄 Moving to next page...")
                time.sleep(2)  # Reduced from 5 seconds
                next_page_found = True
            except:
                pass
        
        return next_page_found
        
    except Exception as e:
        print(f"   ℹ️ No more pages available or pagination error: {str(e)[:50]}")
        return False


def scrape_all_pages_with_details():
    """Scrape all pages with detailed information"""
    all_listings = []
    page_number = 1
    
    while True:
        print(f"\n   📖 Scraping page {page_number}...")
        
        # Scrape current page
        try:
            listings = scrape_listings_with_details()
            if listings:
                all_listings.extend(listings)
                print(f"   ✅ Found {len(listings)} listings on page {page_number}")
            else:
                print(f"   ⚠️ No listings found on page {page_number}")
                break
        except Exception as e:
            print(f"   ⚠️ Error scraping page {page_number}: {str(e)[:50]}")
            break
        
        # Try to go to next page
        if not get_next_page():
            print(f"   ℹ️ No more pages after page {page_number}")
            break
        
        page_number += 1
        
        # Safety limit to prevent infinite loops
        if page_number > 20:
            print(f"   ⚠️ Reached maximum page limit (20)")
            break
    
    print(f"   📊 Total listings scraped across all pages: {len(all_listings)}")
    return all_listings


def scrape_listings_with_details():
    """Enhanced scraping that opens each listing to get full details"""
    wait = WebDriverWait(driver, 10)
    cars = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.deal-card")
    ))

    data = []
    total_cars = len(cars)
    valid_listings = 0

    for idx, car in enumerate(cars, 1):
        def safe_text(selector, multiple=False):
            try:
                if multiple:
                    return [el.text.strip() for el in car.find_elements(By.CSS_SELECTOR, selector)]
                return car.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                return "" if not multiple else []

        title = safe_text(".deal-card__title")
        
        # Skip if this "card" has no title (it's not a real car listing)
        if not title:
            continue
            
        valid_listings += 1
        print(f"   📋 Processing listing {valid_listings}/{total_cars}: {title[:40]}...")
        
        derivative = safe_text(".deal-card__derivative")
        price = safe_text(".deal-card__price")

        details_medium = safe_text(".deal-card__details--body-medium li", multiple=True)
        gearbox, fuel, engine_size = (details_medium + ["", "", ""])[:3]

        details_small = safe_text(".deal-card__details--body-small li", multiple=True)
        distance, year, mileage = (details_small + ["", "", ""])[:3]

        try:
            link = car.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = ""

        # Get detailed information from the listing page
        seller_name, contact_number, car_reg = "", "", ""
        if link:
            print(f"      🔍 Opening listing for details...")
            seller_name, contact_number, car_reg = get_listing_details(link)
            if contact_number:
                print(f"      ✅ Got phone: {contact_number}")
            if seller_name:
                print(f"      ✅ Got dealer: {seller_name}")

        # Determine seller type based on name
        seller_type = "Dealer" if seller_name else "Private"

        data.append([
            CAR_MAKE, POSTCODE, title, derivative, price,
            gearbox, fuel, engine_size, distance, year, mileage,
            seller_name, seller_type, car_reg, contact_number, link
        ])

    return data


def scrape_listings():
    """Original fast scraping without opening each listing"""
    wait = WebDriverWait(driver, 10)
    cars = wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.deal-card")
    ))

    data = []

    for car in cars:
        def safe_text(selector, multiple=False):
            try:
                if multiple:
                    return [el.text.strip() for el in car.find_elements(By.CSS_SELECTOR, selector)]
                return car.find_element(By.CSS_SELECTOR, selector).text.strip()
            except:
                return "" if not multiple else []

        title = safe_text(".deal-card__title")
        derivative = safe_text(".deal-card__derivative")
        price = safe_text(".deal-card__price")

        # Skip if this "card" has no title (it's not a real car listing)
        if not title:
            continue

        details_medium = safe_text(".deal-card__details--body-medium li", multiple=True)
        gearbox, fuel, engine_size = (details_medium + ["", "", ""])[:3]

        details_small = safe_text(".deal-card__details--body-small li", multiple=True)
        distance, year, mileage = (details_small + ["", "", ""])[:3]

        try:
            link = car.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = ""

        # placeholders for now
        seller_name, seller_type, car_reg, contact_number = "", "", "", ""

        data.append([
            CAR_MAKE, POSTCODE, title, derivative, price,
            gearbox, fuel, engine_size, distance, year, mileage,
            seller_name, seller_type, car_reg, contact_number, link
        ])

    return data


def dismiss_popups_and_banners():
    """Try to dismiss any popups, banners, or overlays that might block interaction"""
    try:
        # Common close button selectors
        close_selectors = [
            "button[aria-label*='close']",
            "button[aria-label*='Close']",
            ".close-button",
            ".modal-close",
            ".promotion-banner__close",
            "button.close",
            "[data-dismiss='modal']",
            ".banner-close",
            ".popup-close",
            "svg[aria-label*='close']",
            "button[class*='close']",
            "button[class*='dismiss']"
        ]
        
        for selector in close_selectors:
            try:
                close_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                for btn in close_buttons:
                    if btn.is_displayed():
                        driver.execute_script("arguments[0].click();", btn)
                        print("🔇 Dismissed a popup/banner")
                        time.sleep(0.2)  # Reduced from 0.5 seconds
            except:
                continue
                
        # Also try ESC key to close any modal
        try:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        except:
            pass
            
    except Exception as e:
        pass


def create_driver_with_cookies():
    """Create a new incognito driver instance and load cookies"""
    global driver, wait, actions
    
    # Setup Chrome options with incognito mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--incognito")  # Use incognito mode
    # Add options to reduce detection and improve stability
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    # Create new driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 15)
    actions = ActionChains(driver)
    
    # Navigate to site and load cookies
    driver.get(BASE_URL)
    time.sleep(1)  # Reduced from 2 seconds
    
    # Load cookies if available
    cookies_loaded = load_cookies_if_available()
    
    if cookies_loaded:
        driver.refresh()
        time.sleep(1.5)  # Reduced from 3 seconds
        # Verify login
        page_source = driver.page_source.lower()
        if any(indicator in page_source for indicator in ["sign out", "log out", "my account"]):
            print("✅ Logged in successfully in new window")
    
    # Try to dismiss any initial popups
    dismiss_popups_and_banners()
    
    return driver


def main(postcodes, car_makes, detailed_scraping=True):
    global driver, wait, actions
    all_data = []
    
    scraping_mode = "DETAILED (with phone numbers)" if detailed_scraping else "FAST (no phone numbers)"
    print(f"\n🎯 Starting scraping with incognito windows approach")
    print(f"📊 Mode: {scraping_mode}\n")

    for postcode in postcodes:
        for make in car_makes:
            print(f"\n🚀 Starting scrape for Postcode={postcode}, Make={make}")
            print("🔄 Opening new incognito window...")
            
            # Create a fresh incognito driver for each combination
            driver = create_driver_with_cookies()

            try:
                set_postcode_and_distance(postcode_value=postcode)
                set_age_range()
                set_make(car_make=make)
                set_fuel()

                time.sleep(2)  # Reduced from 5 seconds - let results refresh
                
                # Choose scraping method based on flag
                if detailed_scraping:
                    print("📞 Using detailed scraping with pagination (will open each listing for phone numbers)...")
                    listings = scrape_all_pages_with_details()
                else:
                    print("⚡ Using fast scraping (no phone numbers, single page only)...")
                    listings = scrape_listings()

                # add metadata to results
                for row in listings:
                    row[0] = make      # overwrite CAR_MAKE
                    row[1] = postcode  # overwrite POSTCODE
                    all_data.append(row)

                print(f"✅ Completed scrape for {postcode} + {make} - Found {len(listings)} listings")

            except TimeoutException:
                print(f"❌ Timeout for {postcode} - {make}, skipping...")
            except Exception as e:
                print(f"⚠️ Error scraping {postcode} + {make}: {e}")
            finally:
                # Close this driver instance
                print("🔚 Closing incognito window")
                driver.quit()
                driver = None

    # Write all results once at the end
    with open("carwow_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "car_make","postcode","title","derivative","price",
            "gearbox","fuel","engine_size","distance","year","mileage",
            "seller_name","seller_type","car_reg","contact_number","listing_url"
        ])
        writer.writerows(all_data)

    print(f"\n🎉 Scraping completed! Total listings found: {len(all_data)}")
    print("📁 Data saved to carwow_results.csv")


if __name__ == "__main__":
    postcodes = ["E1 6AN", "M1 1AE", "B1 1AA"]
    car_makes = ["FORD", "BMW", "NISSAN", "RENAULT", "MERCEDES-BENZ"]
    
    # Set to True for detailed scraping with phone numbers (slower)
    # Set to False for fast scraping without phone numbers
    DETAILED_MODE = True
    
    main(postcodes, car_makes, detailed_scraping=DETAILED_MODE)

    print("🎉 All scraping finished")
