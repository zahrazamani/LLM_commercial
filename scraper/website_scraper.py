import requests
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import time
import random
from urllib.parse import urlparse, urljoin
import logging
from config import HEADERS, REQUEST_TIMEOUT, MAX_RETRIES

class WebsiteScraper:
  
    def __init__(self, base_url):
        self.base_url = self._normalize_url(base_url)
        self.domain = urlparse(self.base_url).netloc
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        

    
    def _make_request(self, url):
        """Make request with retry logic and randomized delays."""
        for attempt in range(MAX_RETRIES):
            try:
                # Add slight randomized delay to be respectful to servers
                time.sleep(random.uniform(1, 3))
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt+1}/{MAX_RETRIES}): {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Failed to retrieve {url} after {MAX_RETRIES} attempts")
                    return None
        return None
                
    def get_about_page(self):
        """Find and scrape the about page."""
        about_page_urls = self._find_about_page_url()
        if not about_page_urls:
            logger.warning("Could not find About page")
            return None
            
        about_data = {}
        for url in about_page_urls:
            content = self._scrape_page(url)
            if content:
                about_data[url] = content
                
        return about_data
    
    def _find_about_page_url(self):
        """Find URLs for About pages."""
        response = self._make_request(self.base_url)
        if not response:
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        about_keywords = ['about', 'about us', 'about-us', 'about_us', 'our story', 
                          'our-story', 'who we are', 'company', 'mission']
        
        about_links = []
        
        # Find links in navigation that might point to About pages
        for a_tag in soup.find_all('a', href=True):
            link_text = a_tag.text.strip().lower()
            href = a_tag['href']
            
            if any(keyword in link_text for keyword in about_keywords):
                full_url = urljoin(self.base_url, href)
                if self.domain in urlparse(full_url).netloc:  # Ensure it's on the same domain
                    about_links.append(full_url)
        
        # If no About page found in navigation, try direct common URLs
        if not about_links:
            common_about_paths = ['/about', '/about-us', '/about_us', '/company', '/our-story', '/mission']
            for path in common_about_paths:
                about_links.append(urljoin(self.base_url, path))
                
        return about_links
    
    def _scrape_page(self, url):
        """Scrape content from a given page."""
        response = self._make_request(url)
        if not response:
            return None
            
        # Parse with both BeautifulSoup and selectolax for different extraction strategies
        soup = BeautifulSoup(response.text, 'html.parser')
        select_parser = HTMLParser(response.text)
        
        # Extract title
        title = soup.title.text.strip() if soup.title else ""
        
        # Extract main content
        main_content = self._extract_main_content(soup, select_parser)
        
        # Extract metadata
        meta_description = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and 'content' in meta_tag.attrs:
            meta_description = meta_tag['content']
            
        return {
            'url': url,
            'title': title,
            'meta_description': meta_description,
            'content': main_content,
            'html': response.text  # Store full HTML for later processing if needed
        }
    
    def _extract_main_content(self, soup, select_parser):
        """Extract the main content from the page."""
        # Strategy 1: Look for main content containers
        main_content = ""
        main_elements = soup.find_all(['main', 'article', 'div'], 
                                      class_=['content', 'main-content', 'main', 'about-content'])
        
        if main_elements:
            for element in main_elements:
                main_content += element.get_text(separator=' ', strip=True) + "\n\n"
                
        # Strategy 2: If no content found, try section and other divs
        if not main_content.strip():
            sections = soup.find_all(['section', 'div'], class_=['section', 'container'])
            for section in sections:
                # Skip navigation, footer, sidebar sections
                skip_classes = ['nav', 'navigation', 'menu', 'footer', 'sidebar', 'header']
                if any(cls in section.get('class', []) for cls in skip_classes):
                    continue
                main_content += section.get_text(separator=' ', strip=True) + "\n\n"
                
        # Strategy 3: If still no content, use selectolax to find text nodes
        if not main_content.strip():
            text_nodes = []
            for node in select_parser.css('p, h1, h2, h3, h4, h5, h6, li'):
                if node.text().strip():
                    text_nodes.append(node.text().strip())
            main_content = "\n".join(text_nodes)
            
        # If still no content, fall back to body text
        if not main_content.strip():
            body = soup.find('body')
            if body:
                main_content = body.get_text(separator=' ', strip=True)
                
        return main_content.strip()
    
    def get_products_services(self):
        """Scrape products and services pages."""
        # Similar implementation as get_about_page, targeting product/service pages
        # This would look for links with keywords like 'products', 'services', 'solutions', etc.
        pass
    
    def get_team_info(self):
        """Scrape team/leadership information."""
        # Implementation to find and extract team member information
        pass
        
    def get_company_data(self):
        """Collect all relevant company data."""
        data = {
            'about': self.get_about_page(),
            'products_services': self.get_products_services(),
            'team': self.get_team_info(),
            # Additional data points can be added here
        }
        return data
