"""
WhatsApp Web automation for Maya AI.
Allows sending and reading messages via WhatsApp Web using Selenium.
"""

import os
import time
from typing import Optional, List, Dict
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


class WhatsAppAutomation:
    """WhatsApp Web automation class."""
    
    def __init__(self):
        self.driver = None
        self.wait = None
        self.is_logged_in = False
        
    def start(self, headless: bool = False) -> bool:
        """
        Start WhatsApp Web session.
        
        Args:
            headless: Run browser in headless mode (no UI)
            
        Returns:
            True if started successfully, False otherwise
        """
        if not SELENIUM_AVAILABLE:
            print("[WhatsApp] Selenium not installed. Run: pip install selenium")
            return False
        
        try:
            # Setup Chrome options
            chrome_options = Options()
            
            # User data directory to persist login
            user_data_dir = Path.home() / "AppData" / "Local" / "Maya_WhatsApp_Profile"
            user_data_dir.mkdir(parents=True, exist_ok=True)
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            
            if headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Start browser
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            
            # Open WhatsApp Web
            self.driver.get("https://web.whatsapp.com")
            
            print("[WhatsApp] Browser started. Waiting for login...")
            
            # Wait for QR code or main page
            try:
                # Check if already logged in (main page visible)
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]')))
                self.is_logged_in = True
                print("[WhatsApp] Already logged in!")
                return True
            except TimeoutException:
                print("[WhatsApp] Please scan QR code to log in...")
                # Wait for user to scan QR code (max 60 seconds)
                try:
                    WebDriverWait(self.driver, 60).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
                    )
                    self.is_logged_in = True
                    print("[WhatsApp] Login successful!")
                    return True
                except TimeoutException:
                    print("[WhatsApp] Login timeout. Please try again.")
                    return False
                    
        except Exception as e:
            print(f"[WhatsApp] Failed to start: {e}")
            return False
    
    def send_message(self, contact_name: str, message: str) -> bool:
        """
        Send message to a contact.
        
        Args:
            contact_name: Name of contact or group
            message: Message text to send
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.is_logged_in:
            print("[WhatsApp] Not logged in. Call start() first.")
            return False
        
        try:
            # Search for contact
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(1)
            
            # Click on the contact
            contact = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]'))
            )
            contact.click()
            time.sleep(1)
            
            # Find message input box
            message_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Type message
            message_box.send_keys(message)
            time.sleep(0.5)
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            
            print(f"[WhatsApp] Message sent to {contact_name}: {message}")
            return True
            
        except Exception as e:
            print(f"[WhatsApp] Failed to send message: {e}")
            return False
    
    def read_messages(self, contact_name: str, count: int = 10) -> List[Dict[str, str]]:
        """
        Read recent messages from a contact.
        
        Args:
            contact_name: Name of contact or group
            count: Number of recent messages to read
            
        Returns:
            List of message dictionaries with 'sender' and 'text' keys
        """
        if not self.is_logged_in:
            print("[WhatsApp] Not logged in. Call start() first.")
            return []
        
        try:
            # Search for contact
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(1)
            
            # Click on the contact
            contact = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[@title="{contact_name}"]'))
            )
            contact.click()
            time.sleep(1)
            
            # Get all message elements
            messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-")]')
            
            recent_messages = []
            for msg in messages[-count:]:
                try:
                    # Get message text
                    text_elem = msg.find_element(By.XPATH, './/span[@class="selectable-text copyable-text"]')
                    text = text_elem.text
                    
                    # Determine if incoming or outgoing
                    is_outgoing = "message-out" in msg.get_attribute("class")
                    sender = "You" if is_outgoing else contact_name
                    
                    recent_messages.append({
                        "sender": sender,
                        "text": text
                    })
                except NoSuchElementException:
                    continue
            
            print(f"[WhatsApp] Read {len(recent_messages)} messages from {contact_name}")
            return recent_messages
            
        except Exception as e:
            print(f"[WhatsApp] Failed to read messages: {e}")
            return []
    
    def get_unread_chats(self) -> List[str]:
        """
        Get list of contacts with unread messages.
        
        Returns:
            List of contact names with unread messages
        """
        if not self.is_logged_in:
            print("[WhatsApp] Not logged in. Call start() first.")
            return []
        
        try:
            # Find all chats with unread badge
            unread_elements = self.driver.find_elements(
                By.XPATH, 
                '//div[contains(@class, "unread")]//span[@title]'
            )
            
            unread_contacts = [elem.get_attribute("title") for elem in unread_elements]
            
            print(f"[WhatsApp] Found {len(unread_contacts)} unread chats")
            return unread_contacts
            
        except Exception as e:
            print(f"[WhatsApp] Failed to get unread chats: {e}")
            return []
    
    def stop(self):
        """Stop WhatsApp Web session and close browser."""
        if self.driver:
            try:
                self.driver.quit()
                print("[WhatsApp] Browser closed")
            except Exception as e:
                print(f"[WhatsApp] Error closing browser: {e}")
            finally:
                self.driver = None
                self.is_logged_in = False


# Global instance
_whatsapp_instance: Optional[WhatsAppAutomation] = None


def get_whatsapp() -> WhatsAppAutomation:
    """Get or create WhatsApp automation instance."""
    global _whatsapp_instance
    if _whatsapp_instance is None:
        _whatsapp_instance = WhatsAppAutomation()
    return _whatsapp_instance


def send_whatsapp_message(contact: str, message: str) -> str:
    """
    Send WhatsApp message (convenience function).
    
    Args:
        contact: Contact name
        message: Message text
        
    Returns:
        Status message
    """
    wa = get_whatsapp()
    
    # Start session if not already running
    if not wa.is_logged_in:
        if not wa.start():
            return "Failed to start WhatsApp. Please ensure Chrome is installed and try again."
    
    # Send message
    if wa.send_message(contact, message):
        return f"Message sent to {contact} via WhatsApp"
    else:
        return f"Failed to send message to {contact}"


def read_whatsapp_messages(contact: str, count: int = 10) -> str:
    """
    Read WhatsApp messages (convenience function).
    
    Args:
        contact: Contact name
        count: Number of messages to read
        
    Returns:
        Formatted messages or error message
    """
    wa = get_whatsapp()
    
    # Start session if not already running
    if not wa.is_logged_in:
        if not wa.start():
            return "Failed to start WhatsApp. Please ensure Chrome is installed and try again."
    
    # Read messages
    messages = wa.read_messages(contact, count)
    
    if not messages:
        return f"No messages found from {contact}"
    
    # Format messages
    result = f"Messages from {contact}:\n\n"
    for msg in messages:
        result += f"{msg['sender']}: {msg['text']}\n"
    
    return result


def check_unread_whatsapp() -> str:
    """
    Check for unread WhatsApp messages (convenience function).
    
    Returns:
        List of contacts with unread messages
    """
    wa = get_whatsapp()
    
    # Start session if not already running
    if not wa.is_logged_in:
        if not wa.start():
            return "Failed to start WhatsApp. Please ensure Chrome is installed and try again."
    
    # Get unread chats
    unread = wa.get_unread_chats()
    
    if not unread:
        return "No unread messages"
    
    return f"Unread messages from: {', '.join(unread)}"
