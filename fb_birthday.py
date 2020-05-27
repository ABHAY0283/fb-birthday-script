# coding: utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time,os
from ftplib import FTP
import pickle
from datetime import datetime
from queue import Queue
import sys,subprocess
from threading import Thread

def proxyAuth(path,myProxy):
    try:
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                  singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                  },
                  bypassList: ["foobar.com"]
                }
              };
    
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
    
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """%(myProxy.split('@')[0].split(':')[0],myProxy.split('@')[0].split(':')[1],myProxy.split('@')[1].split(':')[0],myProxy.split('@')[1].split(':')[1])
        # print (background_js)
        pluginName=''.join(random.choice(string.ascii_lowercase) for i in range(10))
        pluginfile = os.path.join(path,'pr','%s.zip'%(pluginName))
        if os.path.exists(pluginfile):
            if os.name=='nt':
                os.remove(pluginfile)
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        return pluginfile
    except Exception as e:
        er=('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        print (er)


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except (Exception) as e:
                print (e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

class UserAgent:
    def __init__(self):
        self.__doc__=self.__init__.__doc__
    def user(self,nr):
        ul=[]
        # path=os.path.dirname(sys.argv[0])
        br=open(os.path.join(path,'mods','user-agents','browsers.txt'),'r').read().splitlines()
        osa=open(os.path.join(path,'mods','user-agents','os-desktop.txt'),'r').read().splitlines()
        appleweb=['534.46','537.36','537.75.14','534.46','534.46','534.46','534.46']
        for x in range(nr):
            u='Mozilla/5.0 (%s) AppleWebKit/%s (KHTML, like Gecko) %s'%(random.choice(osa),random.choice(appleweb),random.choice(br))
            user_agent=parse(u)
            #print str(u)+'.'*30+str(user_agent)
            ul.append(str(u)+'||'+str(user_agent))
        return ul

def loginFb(email,password):

    url='https://www.facebook.com/index.php'

    #### saving + loading account cookie
    path=os.path.dirname(os.path.abspath(__file__))
    if os.path.isfile(os.path.join(path,'cookies',"%s_cookie.pkl"%(email))):
        driver.get(url)
        cookies = pickle.load(open(os.path.join(path,'cookies',"%s_cookie.pkl"%(email)), "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        # print ('loading cookie')
    else:
        driver.get(url)
        pickle.dump( driver.get_cookies() , open(os.path.join(path,'cookies',"%s_cookie.pkl"%(email)),"wb"))
        # print ('saving cookie')
    # driver.implicitly_wait(1)
    # email = WebDriverWait(driver, 25).until(lambda driver : driver.find_element_by_css_selector('input[id="email"]'))
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_xpath('//input[@name="pass"]').send_keys(password)
    driver.find_element_by_xpath('//input[@name="pass"]').send_keys(Keys.ENTER)
    # driver.find_element_by_css_selector('#loginbutton').click()
    driver.implicitly_wait(2)
    search = WebDriverWait(driver, 25).until(lambda driver : driver.find_element_by_css_selector('input[data-testid="search_input"]'))
    # driver.save_screenshot(t'testing1.png')


def logout():
    driver.find_element_by_css_selector('a[id="pageLoginAnchor"]').click()
    time.sleep(1)
    logoutB = WebDriverWait(driver, 25).until(lambda driver : driver.find_element_by_xpath(".//*[@id='BLUE_BAR_ID_DO_NOT_USE']/div/div/div[1]/div/div/ul/li[19]/a"))
    driver.find_element_by_xpath(".//*[@id='BLUE_BAR_ID_DO_NOT_USE']/div/div/div[1]/div/div/ul/li[19]/a").click()

def times():
    today = str(datetime.today()).split(' ')
    time=today[1].split('.')
    t="["+today[0]+' '+time[0]+']'
    return t


if __name__=="__main__":
    path=os.path.dirname(os.path.abspath(__file__))
    try:
        accountsPath=os.path.join(path,'accounts.txt')
        config=open(os.path.join(path,'config.txt'),'r').readlines()
        accounts=open(accountsPath,'r').readlines()

        post='tralala\nhttp://the-top5.com/go/youre-telling-me-2/'
        group='https://www.facebook.com/groups/1703758346565102/'
        browser="chrome"

        for account in accounts:
            email=account.split(',')[0]
            password=account.split(',')[1]
            proxy=account.split(',')[2]
            proxy_ip=proxy.split(":")[0]
            proxy_port=proxy.split(":")[1]
            proxy_user=proxy.split(":")[2]
            proxy_pass=proxy.split(":")[3]
            # print email,password,proxy_ip,proxy_port,proxy_user

            cookie_file_path = os.path.join(path,'cookie')
            if browser=='chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--disable-gpu')
                chrome_options.accept_untrusted_certs = True
                chrome_options.assume_untrusted_cert_issuer = True
                chrome_options.add_argument('--ignore-certificate-errors')
                chrome_options.add_experimental_option("detach", True)
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                # if invisible == 'yes':
                chrome_options.add_argument("--headless")
                # if incognito == 'yes':
                chrome_options.add_argument("--incognito") ########incognito mode
                chrome_options.add_argument('--no-referrers')
                # if disableFlash == 'yes':
                #     chrome_options.add_argument("--disable-bundled-ppapi-flash")   # Disable internal Flash player
                #     chrome_options.add_argument("--disable-plugins-discovery")     # Disable external Flash player (by not allowing it to load)
                # if randomBrowserSize == 'yes':
                #     chrome_options.add_argument("window-size=%s,%s"%(int(res.split(',')[0]),int(res.split(',')[1])))  ###change window size randomly
                # if disableJS=='yes':  ###disable JS
                #     chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
                # if disableImages  == 'yes':
                #     prefs = {"profile.managed_default_content_settings.images":2} # this will disable image loading in the browser
                #     chrome_options.add_experimental_option("prefs",prefs)  # Added preference into chrome options
                # if useProxy == 'yes':
                #     # print (path)
                #     pluginfile=proxyAuth(path,myProxy)
                #     chrome_options.add_extension(pluginfile)
                # if randomUserAgent=='yes':
                #     chrome_options.add_argument("user-agent=%s"%(userAgent))
                if os.name == 'posix':
                    executable_path=os.path.join(path, 'browsers', 'chromedriver')
                    os.system('sudo chmod 777 %s'%executable_path)
                if os.name == 'posix':
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    executable_path=os.path.join(path, 'browsers', 'chromedriver')
                    os.system('sudo chmod 777 %s'%executable_path)
                if os.name == 'nt':
                    executable_path=os.path.join(path, 'browsers', 'chromedriverBK.exe')
                driver = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
            if browser=="Phantomjs":
                dcap = dict(DesiredCapabilities.PHANTOMJS)
                dcap["phantomjs.page.settings.userAgent"] =("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36")
                service_args=['--ssl-protocol=any',
                              '--ignore-ssl-errors=true',
                              '--cookies-file={}'.format(cookie_file_path),
                              '--proxy=%s:%s'%(proxy_ip,proxy_port),
                              '--proxy-auth=%s:%s'%(proxy_user,proxy_pass)
                              ]
                if os.name=="nt":
                    phantomPath=os.path.join(path,"Settings",'phantomjs.exe')
                    driver = webdriver.PhantomJS(executable_path=r"%s"%(phantomPath),desired_capabilities=dcap,service_args=service_args)
                elif os.name=="posix":
                    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=service_args)
            # driver.get('htts://google.com')
            while True:
                try:
                    loginFb(email,password)
                    break
                except:
                    pass
            driver.get("https://www.facebook.com/events/birthdays/")
            driver.implicitly_wait(3)
            nr=0
            if "Write a birthday wish on her timeline..." in driver.page_source or "Write a birthday wish on his timeline..." in driver.page_source:
                try:
                    cc2=driver.find_elements_by_css_selector('textarea[title="Write a birthday wish on her timeline..."]')
                    for c in cc2:
                        c.click()
                        c.send_keys("Happy Birthday!")
                        c.send_keys(Keys.ENTER)
                        nr+=1
                except:
                    pass
                try:
                    cc=driver.find_elements_by_css_selector('textarea[title="Write a birthday wish on his timeline..."]')
                    for c in cc:
                        c.click()
                        c.send_keys("Happy Birthday!")
                        c.send_keys(Keys.ENTER)
                        nr+=1
                except:
                    pass
            driver.save_screenshot('birthday.png')
            time.sleep(1)
            driver.close()
            # close shit
            path=os.path.dirname(sys.argv[0])
            CREATE_NO_WINDOW = 0x08000000
            try:
                subprocess.call('taskkill /F /IM chromedriverBK.exe', creationflags=CREATE_NO_WINDOW)
            except:
                pass
            try:
                subprocess.call('taskkill /F /IM conhost.exe', creationflags=CREATE_NO_WINDOW)
            except:
                pass
            t=times()
            log="%s Today's Birtday Wishes: %s Done!\n"%(t,nr)
            print(log)
            open(os.path.join(path,'birthday.log'),'a').write(log)


    except (Exception) as e:
        er=('Error {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        log="%s %s\n"%(times(),str(er))
        open(os.path.join(path,'birthday.log'),'a').write(log)