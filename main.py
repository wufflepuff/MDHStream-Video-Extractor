import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess
import re
import sys
import json # Import json for config handling

CONFIG_FILE = "config.json"

# --- Language Strings ---
LANG_DE = {
    "welcome": "MDHStream Video Extractor",
    "choose_language": "Sprache wählen / Choose Language",
    "search_prompt": "Suchbegriff (Darsteller/Titel): ",
    "fetching_total": "Ermittle Gesamtanzahl der Videos...",
    "no_videos_found": "Keine Videos für diesen Suchbegriff gefunden oder Zählung fehlgeschlagen.",
    "total_videos_found": "Insgesamt {total} Videos gefunden.",
    "error_initial_connection": "Fehler bei der initialen Verbindung oder Zählung: {e}",
    "choose_mode": "\nWähle einen Download-Modus:",
    "mode_1": "  1: Alle Videos herunterladen",
    "mode_2": "  2: Einen Bereich von Videos herunterladen (z.B. 10-25)",
    "mode_3": "  3: Bestimmte Videos auswählen (z.B. 1, 5, 12)",
    "mode_prompt": "Auswahl (1/2/3): ",
    "invalid_mode": "Ungültige Auswahl, bitte 1, 2 oder 3 eingeben.",
    "scraping_metadata": "\nSammle Video-Metadaten (Titel und URLs)...",
    "metadata_failed": "Konnte keine Video-Metadaten sammeln. Abbruch.",
    "mode_1_selected": "Modus 1: Alle {count} Videos werden heruntergeladen.",
    "mode_2_selected": "Modus 2: Bereich auswählen.",
    "range_prompt": "Gib den Bereich ein (z.B. 10-25), von 1 bis {total}: ",
    "range_selected": "{count} Videos im Bereich {start}-{end} ausgewählt.",
    "invalid_range": "Ungültiger Bereich. Bitte gib Start und Ende zwischen 1 und {total} an, wobei Start <= Ende.",
    "invalid_input_format": "Ungültige Eingabe. Bitte im Format Start-Ende eingeben (z.B. 10-25).",
    "error_range_input": "Ein Fehler ist aufgetreten bei der Bereichseingabe: {e}",
    "mode_3_selected": "Modus 3: Bestimmte Videos auswählen.",
    "indices_prompt": "Gib die Video-Nummern ein, getrennt durch Kommas (z.B. 1, 5, 12), von 1 bis {total}: ",
    "indices_selected": "{count} spezifische Videos ausgewählt.",
    "warning_invalid_indices": "Warnung: Ungültige oder außerhalb des Bereichs liegende Eingaben ignoriert: {invalid_list}",
    "no_valid_indices": "Keine gültigen Video-Nummern eingegeben. Bitte erneut versuchen.",
    "error_indices_input": "Ein Fehler ist aufgetreten bei der Eingabe spezifischer Videos: {e}",
    "no_videos_selected": "Keine Videos zum Herunterladen ausgewählt. Abbruch.",
    "starting_download": "\nStarte Download für {count} ausgewählte Videos nach '{path}'...",
    "processing_video": "\n[{current}/{total_all}] Verarbeite: {title}",
    "page_url": "  Seiten-URL: {url}",
    "checking_exists": "  Prüfe ob Video existiert...",
    "video_exists": "  Video '{filename}' existiert bereits. Übersprungen.",
    "error_checking_file": "  Fehler beim Prüfen, ob die Datei existiert: {e}",
    "extracting_url": "  Extrahiere Video URL...",
    "video_url_found": "  Video URL gefunden: {url}",
    "starting_yt_dlp": "  Starte Download mit yt-dlp...",
    "download_progress": "  Download Fortschritt: {percentage:>6}",
    "download_success": "  Download erfolgreich abgeschlossen für '{title}'",
    "download_failed": "  Download fehlgeschlagen mit Exit-Code {code}",
    "error_yt_dlp_stderr": "  Fehlermeldung:\n{stderr}",
    "error_yt_dlp_not_found": "  Fehler: '{command}' wurde nicht gefunden. Stelle sicher, dass es installiert und im Systempfad ist.",
    "error_unexpected_download": "  Unerwarteter Download-Fehler: {e}",
    "no_video_url_found": "  Keine Video-URL für dieses Video gefunden. Übersprungen.",
    "all_videos_processed": "\nAlle ausgewählten Videos verarbeitet.",
    "summary_success": "Erfolgreiche Downloads: {count}",
    "summary_skipped": "Übersprungene Downloads (bereits vorhanden): {count}",
    "summary_failed": "Fehlgeschlagene Downloads (Fehler/keine URL): {count}",
    "main_menu": "\nHauptmenü:",
    "menu_1_search": "  1: Suche starten / Download",
    "menu_2_settings": "  2: Einstellungen",
    "menu_3_exit": "  3: Beenden",
    "menu_prompt": "Auswahl (1/2/3): ",
    "invalid_menu_choice": "Ungültige Auswahl.",
    "settings_menu": "\nEinstellungen:",
    "settings_1_language": "  1: Sprache ändern (Aktuell: {lang})",
    "settings_2_dl_path": "  2: Download-Pfad ändern (Aktuell: {path})",
    "settings_3_ublock_path": "  3: uBlock Origin Pfad ändern (Aktuell: {path})",
    "settings_4_back": "  4: Zurück zum Hauptmenü",
    "settings_prompt": "Auswahl (1-4): ",
    "enter_new_dl_path": "Neuen Download-Pfad eingeben: ",
    "enter_new_ublock_path": "Neuen Pfad zur uBlock Origin .xpi Datei eingeben: ",
    "path_not_exist": "Pfad '{path}' existiert nicht.",
    "path_not_dir": "Pfad '{path}' ist kein Verzeichnis.",
    "path_not_file": "Pfad '{path}' ist keine Datei.",
    "path_not_xpi": "Datei '{path}' ist keine .xpi Datei.",
    "settings_saved": "Einstellungen gespeichert.",
    "ublock_warning_install": "Warnung: Konnte Erweiterung '{path}' im Headless-Modus nicht installieren: {e}",
    "ublock_warning_not_found": "Warnung: Erweiterungspfad nicht gefunden: '{path}'",
    "goodbye": "Auf Wiedersehen!",
    "scraping_page_metadata": "Scanne Metadaten von Seite {page} ({url})...",
    "error_loading_page": "Fehler beim Laden von Seite {page}: {e}",
    "no_more_videos_on_page": "Keine weiteren Videos auf Seite {page} gefunden oder Fehler beim Scrapen.",
    "collected_so_far": "Bisher gesammelt: {collected} / {total}",
    "metadata_collection_complete": "Metadaten-Sammlung abgeschlossen. {count} Videos gefunden.",
    "error_metadata_collection": "Schwerwiegender Fehler beim Sammeln der Metadaten: {e}",
    "video_blocks_found": "{count} Video-Blöcke auf dieser Seite gefunden.",
    "skipping_block_missing_data": "Überspringe Block bei Index {index}: Titel oder URL fehlt.",
    "error_extracting_block": "Fehler beim Extrahieren eines Video-Blocks (Index ca. {index}): {e}",
    "error_scraping_page": "Fehler beim Scrapen der Seite: {e}",
    "direct_video_tag_found": "Video-URL direkt im <video>-Tag gefunden.",
    "no_direct_video_tag": "Kein direktes <video>-Tag gefunden oder keine 'src' vorhanden, versuche Seitenquelltext-Analyse des Players.",
    "url_found_in_player": "URL im kvs-player div gefunden: {url}",
    "no_url_in_player": "Keine URL im kvs-player div gefunden.",
    "no_player_div": "Kein kvs-player div im Seitenquelltext gefunden.",
    "no_playable_url_found": "Keine abspielbare Video-URL gefunden.",
    "error_extracting_video_url": "Fehler beim Extrahieren der Video-URL von {page_url}: {e}",
    "info_extract_video_count_failed": "Info: Konnte die Videoanzahl nicht aus '{text}' extrahieren.",
    "error_counting_videos": "Fehler bei der Zählung der Gesamtvideos: {e}",
}

LANG_EN = {
    "welcome": "MDHStream Video Extractor",
    "choose_language": "Choose Language / Sprache wählen",
    "search_prompt": "Search term (Actor/Title): ",
    "fetching_total": "Fetching total number of videos...",
    "no_videos_found": "No videos found for this search term or counting failed.",
    "total_videos_found": "Found {total} videos in total.",
    "error_initial_connection": "Error during initial connection or counting: {e}",
    "choose_mode": "\nSelect Download Mode:",
    "mode_1": "  1: Download all videos",
    "mode_2": "  2: Download a range of videos (e.g., 10-25)",
    "mode_3": "  3: Select specific videos (e.g., 1, 5, 12)",
    "mode_prompt": "Choice (1/2/3): ",
    "invalid_mode": "Invalid choice, please enter 1, 2, or 3.",
    "scraping_metadata": "\nScraping video metadata (titles and URLs)...",
    "metadata_failed": "Could not scrape video metadata. Aborting.",
    "mode_1_selected": "Mode 1: All {count} videos will be downloaded.",
    "mode_2_selected": "Mode 2: Select range.",
    "range_prompt": "Enter the range (e.g., 10-25), from 1 to {total}: ",
    "range_selected": "{count} videos selected in range {start}-{end}.",
    "invalid_range": "Invalid range. Please enter start and end between 1 and {total}, with start <= end.",
    "invalid_input_format": "Invalid input format. Please enter in Start-End format (e.g., 10-25).",
    "error_range_input": "An error occurred while entering the range: {e}",
    "mode_3_selected": "Mode 3: Select specific videos.",
    "indices_prompt": "Enter the video numbers, separated by commas (e.g., 1, 5, 12), from 1 to {total}: ",
    "indices_selected": "{count} specific videos selected.",
    "warning_invalid_indices": "Warning: Invalid or out-of-range inputs ignored: {invalid_list}",
    "no_valid_indices": "No valid video numbers entered. Please try again.",
    "error_indices_input": "An error occurred while entering specific videos: {e}",
    "no_videos_selected": "No videos selected for download. Aborting.",
    "starting_download": "\nStarting download for {count} selected videos to '{path}'...",
    "processing_video": "\n[{current}/{total_all}] Processing: {title}",
    "page_url": "  Page URL: {url}",
    "checking_exists": "  Checking if video exists...",
    "video_exists": "  Video '{filename}' already exists. Skipped.",
    "error_checking_file": "  Error checking if file exists: {e}",
    "extracting_url": "  Extracting video URL...",
    "video_url_found": "  Video URL found: {url}",
    "starting_yt_dlp": "  Starting download with yt-dlp...",
    "download_progress": "  Download progress: {percentage:>6}",
    "download_success": "  Download completed successfully for '{title}'",
    "download_failed": "  Download failed with exit code {code}",
    "error_yt_dlp_stderr": "  Error message:\n{stderr}",
    "error_yt_dlp_not_found": "  Error: '{command}' not found. Make sure it is installed and in the system PATH.",
    "error_unexpected_download": "  Unexpected download error: {e}",
    "no_video_url_found": "  No video URL found for this video. Skipped.",
    "all_videos_processed": "\nAll selected videos processed.",
    "summary_success": "Successful downloads: {count}",
    "summary_skipped": "Skipped downloads (already exist): {count}",
    "summary_failed": "Failed downloads (error/no URL): {count}",
    "main_menu": "\nMain Menu:",
    "menu_1_search": "  1: Start Search / Download",
    "menu_2_settings": "  2: Settings",
    "menu_3_exit": "  3: Exit",
    "menu_prompt": "Choice (1/2/3): ",
    "invalid_menu_choice": "Invalid choice.",
    "settings_menu": "\nSettings:",
    "settings_1_language": "  1: Change Language (Current: {lang})",
    "settings_2_dl_path": "  2: Change Download Path (Current: {path})",
    "settings_3_ublock_path": "  3: Change uBlock Origin Path (Current: {path})",
    "settings_4_back": "  4: Back to Main Menu",
    "settings_prompt": "Choice (1-4): ",
    "enter_new_dl_path": "Enter new download path: ",
    "enter_new_ublock_path": "Enter new path to uBlock Origin .xpi file: ",
    "path_not_exist": "Path '{path}' does not exist.",
    "path_not_dir": "Path '{path}' is not a directory.",
    "path_not_file": "Path '{path}' is not a file.",
    "path_not_xpi": "File '{path}' is not an .xpi file.",
    "settings_saved": "Settings saved.",
    "ublock_warning_install": "Warning: Could not install extension '{path}' in headless mode: {e}",
    "ublock_warning_not_found": "Warning: Extension path not found: '{path}'",
    "goodbye": "Goodbye!",
    "scraping_page_metadata": "Scraping metadata from page {page} ({url})...",
    "error_loading_page": "Error loading page {page}: {e}",
    "no_more_videos_on_page": "No more videos found on page {page} or scraping error.",
    "collected_so_far": "Collected so far: {collected} / {total}",
    "metadata_collection_complete": "Metadata collection complete. {count} videos found.",
    "error_metadata_collection": "Fatal error during metadata collection: {e}",
    "video_blocks_found": "{count} video blocks found on this page.",
    "skipping_block_missing_data": "Skipping block at index {index}: Title or URL missing.",
    "error_extracting_block": "Error extracting a video block (index approx. {index}): {e}",
    "error_scraping_page": "Error scraping page: {e}",
    "direct_video_tag_found": "Video URL found directly in <video> tag.",
    "no_direct_video_tag": "No direct <video> tag found or no 'src' present, trying page source analysis of the player.",
    "url_found_in_player": "URL found in kvs-player div: {url}",
    "no_url_in_player": "No URL found in kvs-player div.",
    "no_player_div": "No kvs-player div found in page source.",
    "no_playable_url_found": "No playable video URL found.",
    "error_extracting_video_url": "Error extracting video URL from {page_url}: {e}",
    "info_extract_video_count_failed": "Info: Could not extract video count from '{text}'.",
    "error_counting_videos": "Error counting total videos: {e}",
}

LANG = LANG_EN # Default to English initially

# --- Config Functions ---
def load_config():
    global LANG
    default_config = {
        "language": None, # Will prompt user if None
        "download_path": ".",
        "ublock_path": ""
    }
    if not os.path.exists(CONFIG_FILE):
        save_config(default_config)
        return default_config

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # Ensure all keys exist, add defaults if missing
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            # Set language based on config
            set_language(config.get("language", "en")) # Default to EN if invalid value
            return config
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading config file ({CONFIG_FILE}): {e}. Using defaults.")
        # Attempt to save default config if loading failed badly
        try:
            save_config(default_config)
        except IOError as save_e:
             print(f"Failed to save default config: {save_e}")
        set_language(default_config["language"]) # Set language from default
        return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    except IOError as e:
        print(f"Error saving config file ({CONFIG_FILE}): {e}")

def set_language(lang_code):
    global LANG
    if lang_code and lang_code.lower() == 'de':
        LANG = LANG_DE
        return 'de'
    else:
        LANG = LANG_EN
        return 'en'

def choose_initial_language():
    while True:
        print("\n" + LANG_DE["choose_language"]) # Show in both languages initially
        print("  1: Deutsch (German)")
        print("  2: English")
        choice = input("Auswahl / Choice (1/2): ").strip()
        if choice == '1':
            return 'de'
        elif choice == '2':
            return 'en'
        else:
            print("Ungültige Auswahl / Invalid choice.")

# --- Selenium and Scraping Functions ---
def create_driver(config):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("profile.default_content_settings.popups", 0)
    options.set_preference("xpinstall.signatures.required", False)

    driver = webdriver.Firefox(options=options)

    extension_path = config.get("ublock_path", "")
    if extension_path and os.path.exists(extension_path):
        try:
            driver.install_addon(extension_path, temporary=True)
        except Exception as e:
            print(LANG["ublock_warning_install"].format(path=extension_path, e=e))
    elif extension_path: # Only warn if path was set but not found
        print(LANG["ublock_warning_not_found"].format(path=extension_path))

    return driver

def get_total_videos(driver):
    try:
        widget = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "widget-title"))
        )
        match = re.search(r'(\d+)\s+videos\s+found', widget.text, re.IGNORECASE)
        if match:
            return int(match.group(1))
        print(LANG["info_extract_video_count_failed"].format(text=widget.text))
        return 0
    except Exception as e:
        print(LANG["error_counting_videos"].format(e=e))
        return 0

def scrape_videos_from_page(driver, start_index):
    videos = []
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 5
        while scroll_attempts < max_scroll_attempts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1

        blocks = driver.find_elements(By.CLASS_NAME, "video-block")
        # print(LANG["video_blocks_found"].format(count=len(blocks))) # Optional debug

        current_index = start_index
        for block in blocks:
            try:
                title_element = block.find_element(By.CLASS_NAME, "title")
                title = title_element.text.strip()
                link_element = block.find_element(By.CSS_SELECTOR, "a.infos")
                url = link_element.get_attribute("href")
                if title and url:
                    videos.append({'original_index': current_index, 'title': title, 'url': url})
                    current_index += 1
                else:
                     print(LANG["skipping_block_missing_data"].format(index=current_index))
            except Exception as e:
                print(LANG["error_extracting_block"].format(index=current_index, e=e))
    except Exception as e:
        print(LANG["error_scraping_page"].format(e=e))
    return videos

def extract_video_url(driver, page_url): # Renamed from extract_mp4_url
    try:
        driver.get(page_url)
        time.sleep(3)
        try:
            video_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
            src = video_element.get_attribute("src")
            if src:
                 print(LANG["direct_video_tag_found"])
                 return src
        except:
            print(LANG["no_direct_video_tag"])

        page_source = driver.page_source
        kvs_player_match = re.search(r'<div class="kvs-player".*?>(.*?)</div>', page_source, re.DOTALL)
        if kvs_player_match:
            player_content = kvs_player_match.group(1)
            urls_in_player = re.findall(r'["\'](https?://[^\s<>"\']+)["\']', player_content)
            if not urls_in_player:
                 urls_in_player = re.findall(r'https?://[^\s<>"\']+', player_content)
            if urls_in_player:
                print(LANG["url_found_in_player"].format(url=urls_in_player[0]))
                return urls_in_player[0]
            else:
                print(LANG["no_url_in_player"])
        else:
            print(LANG["no_player_div"])

        print(LANG["no_playable_url_found"])
        return None
    except Exception as e:
        print(LANG["error_extracting_video_url"].format(page_url=page_url, e=e))
        return None

def scrape_all_video_metadata(search_url, total_videos, config):
    if total_videos <= 0:
        return []

    driver = create_driver(config)
    try:
        results = []
        page = 1
        collected_count = 0

        while collected_count < total_videos:
            if page == 1:
                url = search_url
            else:
                base_url, query = search_url.split('?', 1) if '?' in search_url else (search_url, '')
                if base_url.endswith('/'):
                    base_url = base_url[:-1]
                url = f"{base_url}/page/{page}/"
                if query:
                    url += f"?{query}"

            print(LANG["scraping_page_metadata"].format(page=page, url=url))
            try:
                driver.get(url)
                time.sleep(1)
            except Exception as e:
                print(LANG["error_loading_page"].format(page=page, e=e))
                break

            page_videos = scrape_videos_from_page(driver, collected_count + 1)

            if not page_videos:
                 print(LANG["no_more_videos_on_page"].format(page=page))
                 break

            needed = total_videos - collected_count
            results.extend(page_videos[:needed])
            collected_count = len(results)

            print(LANG["collected_so_far"].format(collected=collected_count, total=total_videos))

            if collected_count >= total_videos:
                break

            page += 1
            time.sleep(1.5)

        print(LANG["metadata_collection_complete"].format(count=len(results)))
        return results
    except Exception as e:
        print(LANG["error_metadata_collection"].format(e=e))
        return []
    finally:
        if driver:
            driver.quit()

# --- Core Application Logic ---
def start_download_process(config):
    search_term = input(LANG["search_prompt"]).strip()
    if not search_term:
        return # Go back to menu if no search term

    safe_search_term = re.sub(r'[\\/*?:"<>|]', "_", search_term).strip()
    if not safe_search_term:
        safe_search_term = "downloaded_videos"
    search_url = f"https://mdhstream.cc/?s={search_term}"

    print(LANG["fetching_total"])
    driver_count = create_driver(config)
    total = 0
    try:
        driver_count.get(search_url)
        total = get_total_videos(driver_count)
        if not total:
            print(LANG["no_videos_found"])
            return
        print(LANG["total_videos_found"].format(total=total))
    except Exception as e:
         print(LANG["error_initial_connection"].format(e=e))
         return
    finally:
        if driver_count:
            driver_count.quit()

    # --- Mode Selection ---
    mode = ''
    while mode not in ['1', '2', '3']:
        print(LANG["choose_mode"])
        print(LANG["mode_1"])
        print(LANG["mode_2"])
        print(LANG["mode_3"])
        mode = input(LANG["mode_prompt"]).strip()
        if mode not in ['1', '2', '3']:
            print(LANG["invalid_mode"])

    # --- Directory Setup (using config) ---
    base_download_dir = config.get("download_path", ".")
    download_dir = os.path.join(base_download_dir, safe_search_term)

    try:
        os.makedirs(download_dir, exist_ok=True)
        # No need to print path here, it's in settings
    except OSError as e:
        print(f"Error creating directory '{download_dir}': {e}") # Keep error in EN for now
        print("Saving to current directory instead.")
        download_dir = "."

    # --- Scrape Metadata ---
    print(LANG["scraping_metadata"])
    all_metadata = scrape_all_video_metadata(search_url, total, config)

    if not all_metadata:
        print(LANG["metadata_failed"])
        return

    # --- Filter Videos Based on Mode ---
    videos_to_download = []
    if mode == '1':
        print(LANG["mode_1_selected"].format(count=len(all_metadata)))
        videos_to_download = all_metadata
    elif mode == '2':
        print(LANG["mode_2_selected"])
        while True:
            try:
                range_input = input(LANG["range_prompt"].format(total=total)).strip()
                if not range_input: continue
                start_str, end_str = range_input.split('-')
                start_index = int(start_str.strip())
                end_index = int(end_str.strip())
                if 1 <= start_index <= end_index <= total:
                    videos_to_download = [v for v in all_metadata if start_index <= v['original_index'] <= end_index]
                    print(LANG["range_selected"].format(count=len(videos_to_download), start=start_index, end=end_index))
                    break
                else:
                    print(LANG["invalid_range"].format(total=total))
            except ValueError:
                print(LANG["invalid_input_format"])
            except Exception as e:
                 print(LANG["error_range_input"].format(e=e))
    elif mode == '3':
        print(LANG["mode_3_selected"])
        while True:
            try:
                indices_input = input(LANG["indices_prompt"].format(total=total)).strip()
                if not indices_input: continue
                indices_str = indices_input.split(',')
                specific_indices = set()
                invalid_inputs = []
                for i_str in indices_str:
                    try:
                        index = int(i_str.strip())
                        if 1 <= index <= total:
                            specific_indices.add(index)
                        else:
                            invalid_inputs.append(i_str.strip())
                    except ValueError:
                        invalid_inputs.append(i_str.strip())

                if invalid_inputs:
                    print(LANG["warning_invalid_indices"].format(invalid_list=', '.join(invalid_inputs)))

                if not specific_indices:
                     print(LANG["no_valid_indices"])
                     continue

                videos_to_download = [v for v in all_metadata if v['original_index'] in specific_indices]
                videos_to_download.sort(key=lambda x: x['original_index'])
                print(LANG["indices_selected"].format(count=len(videos_to_download)))
                break
            except Exception as e:
                 print(LANG["error_indices_input"].format(e=e))

    if not videos_to_download:
        print(LANG["no_videos_selected"])
        return

    # --- Download Loop ---
    print(LANG["starting_download"].format(count=len(videos_to_download), path=os.path.abspath(download_dir)))
    driver_dl = create_driver(config)

    download_success_count = 0
    download_fail_count = 0
    download_skip_count = 0

    try:
        for video in videos_to_download:
            print(LANG["processing_video"].format(current=video['original_index'], total_all=total, title=video['title']))

            # --- Check if video already exists ---
            try:
                safe_title = re.sub(r'[\\/*?:"<>|]', "_", video['title']).strip()
                if not safe_title:
                    safe_title = f"video_{video['original_index']}"

                file_exists = False
                # print(LANG["checking_exists"]) # Optional verbose output
                if os.path.exists(download_dir):
                    for filename in os.listdir(download_dir):
                        if filename.startswith(safe_title + '.') and not filename.endswith(('.part', '.ytdl')):
                            file_exists = True
                            print(LANG["video_exists"].format(filename=filename))
                            break

                if file_exists:
                    download_skip_count += 1
                    continue

            except Exception as e:
                print(LANG["error_checking_file"].format(e=e))
                download_fail_count += 1
                continue

            # --- Proceed with URL extraction and download ---
            print(LANG["page_url"].format(url=video['url']))
            # print(LANG["extracting_url"]) # Optional verbose output
            video_url_to_download = extract_video_url(driver_dl, video['url'])

            if video_url_to_download:
                print(LANG["video_url_found"].format(url=video_url_to_download))
                try:
                    output_template = os.path.join(download_dir, f'{safe_title}.%(ext)s')
                    print(LANG["starting_yt_dlp"])
                    command = ['yt-dlp', '-o', output_template, '--no-warnings', '--progress', video_url_to_download]

                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)

                    last_percentage = "-1%"
                    for line in iter(process.stdout.readline, ''):
                        match = re.search(r'\[download\]\s+(\d+\.\d+)%', line)
                        if match:
                            percentage = match.group(1) + "%"
                            if percentage != last_percentage:
                                print(LANG["download_progress"].format(percentage=percentage.strip()), end='\r')
                                sys.stdout.flush()
                                last_percentage = percentage
                        else: pass # Ignore other yt-dlp output lines

                    process.stdout.close()
                    return_code = process.wait()
                    print() # Newline after progress

                    if return_code == 0:
                        print(LANG["download_success"].format(title=safe_title))
                        download_success_count += 1
                    else:
                        print(LANG["download_failed"].format(code=return_code))
                        download_fail_count += 1
                        stderr_output = process.stderr.read()
                        if stderr_output:
                            print(LANG["error_yt_dlp_stderr"].format(stderr=stderr_output.strip()))
                        process.stderr.close()

                except FileNotFoundError:
                     print(LANG["error_yt_dlp_not_found"].format(command=command[0]))
                     download_fail_count += 1
                     break # Stop if downloader is missing
                except Exception as e:
                    print(LANG["error_unexpected_download"].format(e=e))
                    download_fail_count += 1
                    if 'process' in locals() and process.poll() is None:
                         process.kill(); process.wait()
                         if process.stdout: process.stdout.close()
                         if process.stderr: process.stderr.close()
            else:
                print(LANG["no_video_url_found"])
                download_fail_count += 1

            time.sleep(1)
    finally:
        if driver_dl:
            driver_dl.quit()

    print(LANG["all_videos_processed"])
    print(LANG["summary_success"].format(count=download_success_count))
    print(LANG["summary_skipped"].format(count=download_skip_count))
    print(LANG["summary_failed"].format(count=download_fail_count))
    input("\nDrücke Enter um zum Hauptmenü zurückzukehren / Press Enter to return to main menu...")


def manage_settings(config):
    global LANG
    while True:
        current_lang_code = config.get("language", "en")
        current_lang_name = "Deutsch" if current_lang_code == 'de' else "English"
        current_dl_path = os.path.abspath(config.get("download_path", "."))
        current_ublock_path = config.get("ublock_path", "Nicht gesetzt / Not set")

        print(LANG["settings_menu"])
        print(LANG["settings_1_language"].format(lang=current_lang_name))
        print(LANG["settings_2_dl_path"].format(path=current_dl_path))
        print(LANG["settings_3_ublock_path"].format(path=current_ublock_path))
        print(LANG["settings_4_back"])
        choice = input(LANG["settings_prompt"]).strip()

        if choice == '1':
            new_lang_code = choose_initial_language() # Reuse initial selection prompt
            config["language"] = set_language(new_lang_code)
            save_config(config)
            print(LANG["settings_saved"])
        elif choice == '2':
            new_path = input(LANG["enter_new_dl_path"]).strip()
            if not new_path: continue
            if os.path.isdir(new_path):
                config["download_path"] = new_path
                save_config(config)
                print(LANG["settings_saved"])
            elif not os.path.exists(new_path):
                 print(LANG["path_not_exist"].format(path=new_path))
            else:
                 print(LANG["path_not_dir"].format(path=new_path))
        elif choice == '3':
            new_path = input(LANG["enter_new_ublock_path"]).strip()
            if not new_path: # Allow clearing the path
                config["ublock_path"] = ""
                save_config(config)
                print(LANG["settings_saved"])
                continue
            if os.path.isfile(new_path):
                if new_path.lower().endswith(".xpi"):
                    config["ublock_path"] = new_path
                    save_config(config)
                    print(LANG["settings_saved"])
                else:
                    print(LANG["path_not_xpi"].format(path=new_path))
            elif not os.path.exists(new_path):
                 print(LANG["path_not_exist"].format(path=new_path))
            else:
                 print(LANG["path_not_file"].format(path=new_path))
        elif choice == '4':
            break
        else:
            print(LANG["invalid_menu_choice"])

# --- Main Execution ---
if __name__ == "__main__":
    config = load_config()

    # Initial language selection if not set
    if config.get("language") is None:
        lang_code = choose_initial_language()
        config["language"] = set_language(lang_code)
        save_config(config) # Save the chosen language

    print(LANG["welcome"])

    while True:
        print(LANG["main_menu"])
        print(LANG["menu_1_search"])
        print(LANG["menu_2_settings"])
        print(LANG["menu_3_exit"])
        choice = input(LANG["menu_prompt"]).strip()

        if choice == '1':
            start_download_process(config)
        elif choice == '2':
            manage_settings(config)
            # Reload config in case language changed in settings
            config = load_config()
        elif choice == '3':
            print(LANG["goodbye"])
            break
        else:
            print(LANG["invalid_menu_choice"])