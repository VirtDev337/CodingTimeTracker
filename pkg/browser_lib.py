import json
import os
import re
import time
from urllib import parse

class Browser:
    def __init__(self):
        self.browsers = {
            "Firefox": {},
            "Chrome": {},
            "Brave": {}
        }
        self.current_browser = ""
        self.current_tab = ""

    def start_browser(self, browser_name: str):
        self.current_browser = browser_name
        self.browsers[self.current_browser] = {
            'start_time': 0,
            'end_time': 0,
            'elapsed_time': 0,
            'tabs': {}
        }
        self.browsers[self.current_browser].start_time = time.time()
        self.update_tab()
        print(f"Started tracking {self.current_browser}")

    def end_browser(self):
        self.browsers[self.current_browser]['end_time'] = time.time()
        self.browsers[self.current_browser]['elapsed_time'] = self.browsers[self.current_browser].end_time - self.browsers[self.current_browser].start_time
        if self.current_browser:

            if self.current_tab not in self.browsers[self.current_browser]['tabs']:
                self.browsers[self.current_browser].tabs[self.current_tab] = 0

            self.browsers[self.current_browser].tabs[self.current_tab] += self.browsers[self.current_browser].elapsed_time

            return self.save_browser()

    def valid_url(self, url):
        invalid_pattern = "facebook|fb|meta|twitter|instagram|linkedin|indeed|glassdoor|pinterest|whatsapp|zoom|slack|bufferapp|tumblr|getpocket|citi|wellsfargo|chase|nerdwallet|ally|sofi|.?money.?|.?bank.?|pnc|key|oneunited|fnb-online"
        gov_pattern = ".?\.(gov|mil)"

        if re.match(invalid_pattern, url) or re.match(gov_pattern, url):
            return False

        return True


    def update_tab(self, url: str):
        if self.current_browser:
            parsed_url = parse(url)
            if self.valid_url(parsed_url):
                self.current_tab = parsed_url.netloc
                if self.current_tab not in self.browsers[self.current_browser].tabs:
                    self.browsers[self.current_browser].tabs[self.current_tab]['start_time'] = time.time()
                else:
                    self.browsers[self.current_browser].tabs[self.current_tab]['elapsed_time'] += time.time() - self.browsers[self.current_browser].tabs[self.current_tab].start_time

    def save_browser(self):
        current_browser = self.browsers[self.current_browser]
        active_browsers = {
            current_browser: current_browser.to_dict()
        }

        for browser in self.browsers:
            if len(self.browsers[browser]) > 0 and browser != self.current_browser:
                active_browsers[browser] = browser.to_dict(browser)

        path = os.path.join(
                os.path.expanduser('~'),
                '.codetime',
                'browsers.json'
            )

        with open(path, "w") as file:
                json.dump(
                    active_browsers,
                    file,
                    indent=4,
                    default=str
                )

        print(f"Stopped tracking {self.current_browser}")

    def print_browsers(self):
        for browser_name, browser_data in self.browsers.items:
            print(f"{browser_name}: {browser_data}")

    def to_dict(self, browser=None):
        return {
            time.strftime('%x', time.localtime()): {
                browser or self.current_browser: {
                    'name': browser or self.current_browser,
                    'time_spent': self.browsers[self.current_browser].elapsed_time,
                    'tabs': dict(self.browsers[self.current_browser].tabs)
                }
            }
        }