'''检查chrome浏览器驱动并更新'''
import re
import os
import shutil
import time
import zipfile
import requests
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME_DRIVER_DIR = 'C://Users//admin//AppData//Local//Programs//Python//Python38//chromedriver.exe'


class ChromeDriverCrawler:
    '''更新chrome浏览器驱动'''
    def check_current_version(self):    # pylint: disable=no-self-use
        '''检查驱动是否正常 '''
        try:
            driver = webdriver.Chrome()
            driver.get(url='http://www.qq.com')
            driver.quit()
        except SessionNotCreatedException as err:
            current_version = re.findall('Current browser version is (.*?) with', err.msg)[0]
            if current_version:
                return current_version
        except WebDriverException as err:
            raise err

    def download_url_filter(self, data, key_word):    # pylint: disable=no-self-use
        '''从web标签对象列表中找出下载url'''
        try:
            return [i.get_attribute('href') for i in data if \
            len(re.findall(re.compile(key_word), i.get_attribute('href') > 0))][-1]
        except IndexError:
            return None

    def unzip_copy_driver(self, zip_file_dir):    # pylint: disable=no-self-use
        '''解压并复制浏览器驱动'''
        with zipfile.ZipFile(zip_file_dir, 'r') as myzip:
            myzip.extractall(os.path.join(BASE_DIR, 'tmp'))
        shutil.copy(os.path.join(BASE_DIR, 'tmp/chromedriver.exe'), CHROME_DRIVER_DIR)

    def download_driver(self, chrome_version):    # pylint: disable=no-self-use
        '''下载驱动匹配版本'''
        partial_version = '.'.join(chrome_version.split('.')[:-1])
        driver = webdriver.PhantomJS(executable_path=r'C:/Program Files/phantomjs/bin/phantomjs.exe')
        driver.get('https://chromedriver.storage.googleapis.com/index.html')
        time.sleep(5)
        data = driver.find_elements_by_tag_name('a')
        download_page_url = self.download_url_filter(data, partial_version)
        if download_page_url:
            driver.get(download_page_url)
            time.sleep(5)
            data = driver.find_elements_by_tag_name('a')
            driver.quit()
            file_url = self.download_url_filter(data, 'win32.zip')
            if file_url:
                content = requests.get(file_url).content
                zip_file_name = file_url.split('/')[-1]
                zip_file_dir = os.path.join(BASE_DIR, 'tmp', zip_file_name)
                with open(zip_file_dir, 'wb') as f:
                    f.write(content)
                self.unzip_copy_driver(zip_file_dir)
            else:
                raise 'webdriver not found.Please check https://chromedriver.storage.googleapis.com/index.html manually'
        else:
            raise 'webdriver not found.Please check https://chromedriver.storage.googleapis.com/index.html manually'


def main():
    mng = ChromeDriverCrawler()
    new_version = mng.check_current_version()
    if new_version is not None:
        mng.download_driver(new_version)


if __name__ == '__main__':
    main()
