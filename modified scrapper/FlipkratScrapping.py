import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By
import pandas as pd

from mongoDBOperations import MongoDBManagement


class FlipkratScrapper:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 2, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False

    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            current_window_url = self.driver.current_url
            return current_window_url
        except Exception as e:
            raise Exception(f"(getCurrentWindowUrl) - Something went wrong on retrieving current url.\n" + str(e))

    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))

    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    def findElementByClass(self, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.CLASS_NAME, value=classpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = self.driver.find_elements_by_tag_name(tag_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))

    def findingElementsFromPageUsingClass(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CLASS_NAME, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def findingElementsFromPageUsingCSSSelector(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CSS_SELECTOR, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def openUrl(self, url):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))

    def login_popup_handle(self):
        """
        This function handle/closes the login popup displayed.
        """
        try:
            self.wait()
            locator = self.getLocatorsObject()
            self.findElementByXpath(xpath=locator.getLoginCloseButton()).click()
            return True
        except Exception as e:
            raise Exception("(login_popup_handle) - Failed to handle popup.\n" + str(e))

    def searchProduct(self, searchString):
        """
        This function helps to search product using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea())
            search_box_path.send_keys(searchString)
            search_button = self.findElementByXpath(xpath=locator.getSearchButton())
            search_button.click()
            return True
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(searchProduct) - Something went wrong on searching.\n" + str(e))

    def generateTitle(self, search_string):
        """
        This function generatesTitle for the products searched using search string
        :param search_string: product to be searched for.
        """
        try:
            title = search_string + "- Buy Products Online at Best Price in India - All Categories | Flipkart.com"
            return title
        except Exception as e:
            raise Exception(f"(generateTitle) - Something went wrong while generating complete title.\n" + str(e))

    def getProductLinks(self):
        """
        This function returns all the list of links.
        """
        try:
            links = []
            all_links = self.findElementByTag('a')
            for link in all_links:
                links.append(link.get_attribute('href'))
            count = 0
            for i in links:
                if count > 15: break
                if '?pid=' in i:
                    print(i)
                    count = count + 1
                    yield str(i)
        except Exception as e:
            raise Exception(f"(getProductLinks) - Something went wrong on getting link from the page.")

    def actualProductLinks(self):
        """
        This function returns the actual product links after filtering.
        """
        try:
            productLinks = []
            count = 0
            for link in self.getProductLinks():
                if count > 15: break
                if '?pid=' in link:
                    print(link)
                    productLinks.append(link)
                    count = count + 1
                else:
                    continue
            return productLinks
        except Exception as e:
            raise Exception(f"(actualProductLinks) - Something went wrong while searching the url.\n" + str(e))

    def getLinkForExpectedReviewCount(self, expected_review, searchString):
        """
        This function extracts the link of product having more than expected count.
        """
        try:
            product_links = self.actualProductLinks(searchString=searchString)
            count = 0
            expected_count = self.getExpectedCountForLooping(expected_review=expected_review)
            while count < expected_count:
                url_to_hit = product_links[random.randint(0, len(product_links) - 1)]
                self.openUrl(url=url_to_hit)
                total_review_page = self.getTotalReviewPage()
                count = total_review_page
            self.openUrl(url=url_to_hit)
            return True
        except Exception as e:
            raise Exception(
                f"(getLinkForExpectedReviewCount) - Failed to retrive the link for product having more than "
                f"expectedcount of review.\n" + str(
                    e))

    def checkVisibilityOfElement(self, element_to_be_checked):
        """
        This function check the visibility of element on the webpage
        """
        try:
            if element_to_be_checked in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkVisibilityOfElement) - Not able to check for the element.\n" + str(e))

    def getProductName(self):
        """
        This function helps to retrieve actual name of the product.
        """
        try:
            locator = self.getLocatorsObject()
            element = locator.getProductNameByClass()
            if self.checkVisibilityOfElement(element_to_be_checked=element):
                product_name = self.findElementByClass(classpath=locator.getProductNameByClass()).text
            else:
                product_name = self.findElementByXpath(xpath=locator.getProductNameByXpath()).text
            print(product_name)
            return product_name
        except Exception as e:
            raise Exception(f"(getProductName) - Not able to get the product name.\n" + str(e))

    def getProductSearched(self, search_string):
        """
        This function returns the name of product searched
        """
        try:
            return search_string
        except Exception as e:
            return search_string

    def getPrice(self):
        """
        This function helps to retrieve the original price of the product.
        """
        try:
            locator = self.getLocatorsObject()
            original_price = self.findElementByClass(classpath=locator.getOriginalPriceUsingClass()).text
            print(original_price)
            return original_price
        except Exception as e:
            raise Exception(f"(getPrice) - Not able to get the price of product.\n" + str(e))

    def getDiscountedPercent(self):
        """
        This function returns discounted percent for the product.
        """
        try:
            locator = self.getLocatorsObject()
            discounted_price = self.findElementByClass(classpath=locator.getDiscountPercent()).text
            print(discounted_price)
            return discounted_price
        except Exception as e:
            return "No Discount"

    def checkMoreOffer(self):
        """
        This function checks whether more offer links is provided for the product or not.
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreOffersUsingClass() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkMoreOffer) - Trouble in finding more offer link.\n" + str(e))

    def clickOnMoreOffer(self):
        """
        This function clicks on more offer button.
        """
        try:
            status = self.checkMoreOffer()
            if status:
                locator = self.getLocatorsObject()
                more_offer = self.findElementByClass(classpath=locator.getMoreOffers())
                more_offer.click()
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(clickOnMoreOffer) - Not able to click on more offer button.\n" + str(e))

    def getAvailableOffer(self):
        """
        This function returns offers available
        """
        try:
            status = self.checkMoreOffer()
            locator = self.getLocatorsObject()
            if status:
                self.clickOnMoreOffer()
            if locator.getAvailableOffers()[0] in self.driver.page_source:
                offer_details = self.findElementByClass(classpath=locator.getAvailableOffers()[0]).text
            elif locator.getAvailableOffers()[1] in self.driver.page_source:
                offer_details = self.findElementByClass(classpath=locator.getAvailableOffers()[1]).text
            else:
                offer_details = "No Offer For the product"
            return offer_details
        except Exception as e:
            raise Exception(f"(getAvailableOffer) - Not able to get the offer details of product.\n" + str(e))

    def getOfferDetails(self):
        """
        This function returns the offers in formatted way.
        """
        try:
            available_offers = self.getAvailableOffer()
            split_offers = available_offers.split("\n")
            print(split_offers[1:])
            return split_offers[1:]
        except Exception as e:
            return "No offer Available"

    def checkViewPlanForEMI(self):
        """
        This function returns boolean value for EMI is available or not.
        """
        try:
            # status = self.checkMoreOffer()
            locator = self.getLocatorsObject()
            # if status:
            #     self.clickOnMoreOffer()
            if locator.getViewPlanLinkUsingClass() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkViewPlanForEMI) - Error on finding view plans link for EMI.\n" + str(e))

    def getEMIDetails(self):
        """
        This function returns EMI details of the product.
        """
        try:
            locator = self.getLocatorsObject()
            status = self.checkViewPlanForEMI()
            # if status:
            if locator.getViewPlanLinkUsingClass() in self.driver.page_source:
                emi_detail = self.findElementByXpath(xpath=locator.getEMIDetail()).text
                return emi_detail
            else:
                return "NO EMI Plans"
        except Exception as e:
            return "NO EMI Plans"

    def getTotalReviewPage(self):
        """
        This function retrieves total number of pages available for review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getMoreReviewUsingClass()[0] in self.driver.page_source:
                self.findElementByClass(classpath=locator.getMoreReviewUsingClass()[0]).click()
            elif locator.getMoreReviewUsingClass()[1] in self.driver.page_source:
                self.findElementByClass(classpath=locator.getMoreReviewUsingClass()[1]).click()
            else:
                return int(1)
            total_review_page = [self.findElementByClass(classpath=locator.getTotalReviewPage()).text][0]
            split_values = total_review_page.split("\n")
            value = str(split_values[0]).split()[-1]
            return int(value)
        except Exception as e:
            return int(1)

    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(2)
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))

    def getRatings(self):
        """
        This function gets rating for the product.
        """
        try:
            locator = self.getLocatorsObject()
            rating = self.findingElementsFromPageUsingCSSSelector(locator.getRatings())
            return rating
        except Exception as e:
            raise Exception(f"(getRatings) - Not able to get the rating details of product.\n" + str(e))

    def getComments(self):
        """
        This function gets review comment for the product
        """
        try:
            locator = self.getLocatorsObject()
            comment_object = locator.getComment()
            if comment_object[0] in self.driver.page_source:
                comment = self.findingElementsFromPageUsingClass(comment_object[0])
            else:
                comment = self.findingElementsFromPageUsingClass(comment_object[1])
            return comment
        except Exception as e:
            raise Exception(f"(getComment) - Not able to get the comment details of product.\n" + str(e))

    def getCustomerNamesAndReviewAge(self):
        """
        This function gets customername for the review
        """
        try:
            locator = self.getLocatorsObject()
            customer_name = self.findingElementsFromPageUsingClass(locator.getCustomerName())
            return customer_name
        except Exception as e:
            raise Exception(f"(getCustomerNamesAndReviewAge) - Not able to get the name of product.\n" + str(e))

    def checkForNextPageLink(self):
        """
        This function click on the next page for the review
        """
        try:
            locator = self.getLocatorsObject()
            if locator.getNextFromTotalReviewPage() in self.driver.page_source:
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(checkForNextPageLink) - Not able to click on next button.\n" + str(e))

    def getExpectedCountForLooping(self, expected_review):
        """
        This functoin retrives the total number of pages which should be searched for review
        """
        try:
            expected_count = expected_review / 10
            return int(expected_count)
        except Exception as e:
            raise Exception(f"(getExpectedCountForLooping) - Something went wrong with review count.\n" + str(e))

    def getReviewDetailsForProduct(self):
        """
        This function gets all Review Details for the product
        """
        try:
            ratings, comment, customer_name, review_age = [], [], [], []
            ratings.append([i.text for i in self.getRatings()])
            comment.append([i.text for i in self.getComments()])
            cust_name_and_review_age = [i.text for i in self.getCustomerNamesAndReviewAge()]
            customer_name.append(
                self.separateCustomernameAndReviewAge(list_of_custname_and_reviewage=cust_name_and_review_age)[0])
            review_age.append(
                self.separateCustomernameAndReviewAge(list_of_custname_and_reviewage=cust_name_and_review_age)[1])
            yield ratings, comment, customer_name, review_age
        except Exception as e:
            # self.driver.refresh()
            raise Exception(
                f"(getReviewDetailsForProduct) - Something went wrong on getting details of review for the product.\n" + str(
                    e))

    def separateCustomernameAndReviewAge(self, list_of_custname_and_reviewage):
        """
        This function separates the review age and customer name.
        """
        try:
            customer_name = list_of_custname_and_reviewage[0::2]
            review_age = list_of_custname_and_reviewage[1::2]
            return customer_name, review_age
        except Exception as e:
            raise Exception(f"(separateCustomernameAndReviewAge) - Something went wrong.\n" + str(e))

    def generatingResponse(self, product_searched, product_name, price, discount_percent, offer_details, EMI, result):
        """
        This function generates the final response to send.
        """
        try:
            response_dict = {"product_searched": [], "product_name": [], "price": [], "discount_percent": [],
                             "offer_details": [], "EMI": [], "ratings": [], "comments": [], "customer_name": [],
                             "review_Age": []}
            rating, comments, cust_name, review_age = result[0], result[1], result[2], result[3]
            response_dict["ratings"] = rating
            response_dict["comments"] = comments
            response_dict["customer_name"] = cust_name
            response_dict["review_Age"] = review_age
            response_dict["product_name"] = product_name
            response_dict["product_searched"] = product_searched
            response_dict["offer_details"] = offer_details
            response_dict["EMI"] = EMI
            response_dict["price"] = price
            response_dict["discount_percent"] = discount_percent
            return response_dict
        except Exception as e:
            raise Exception(f"(generatingResponse) - Something went wrong on generating response")

    def generateDataForColumnAndFrame(self, response):
        """
        This function generates data for the column where only single data is presented. And then frames it in data frame.
        """
        try:
            data_frame1 = pd.DataFrame()
            flatten_rating = [j for i in response['ratings'] for j in i]
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    list_value = []
                    for i in range(0, len(flatten_rating)):
                        list_value.append(response[column_name])
                    data_frame1.insert(0, column_name, list_value)
            print(data_frame1)
            return data_frame1
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def frameToDataSet(self, response):
        """
        This function frames the column to dataframe.
        """
        try:
            data_frame2 = pd.DataFrame()
            for column_name, value in response.items():
                if column_name == 'product_searched' or column_name == 'product_name' or column_name == 'price' or column_name == 'discount_percent' or column_name == 'offer_details' or column_name == 'EMI':
                    continue
                else:
                    flatten_result = [values for lists in response[column_name] for values in lists]
                    data_frame2.insert(0, column_name, flatten_result)
            return data_frame2
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))

    def createDataFrameIncludingAllColumn(self, response):
        """
        This function creates dataframe from given data.
        """
        try:
            data_frame1 = self.generateDataForColumnAndFrame(response=response)
            data_frame2 = self.frameToDataSet(response=response)
            frame = [data_frame1, data_frame2]
            data_frame = pd.concat(frame, axis=1)
            return data_frame
        except Exception as e:
            raise Exception(f"(createDataFrame) - Something went wrong on creating data frame.\n" + str(e))

    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))

    def getReviewsToDisplay(self, searchString, expected_review, username, password, review_count):
        """
        This function returns the review and other detials of product
        """
        try:
            search = searchString
            mongoClient = MongoDBManagement(username=username, password=password)
            locator = self.getLocatorsObject()
            for link in self.getProductLinks():
                print('reviewing: ' + str(review_count))
                if review_count <= expected_review:
                    self.openUrl(url=link)
                    if locator.getCustomerName() in self.driver.page_source:
                        product_name = self.getProductName()
                        print(product_name)
                        db_search = mongoClient.findfirstRecord(db_name="Flipkart-Scrapper",
                                                                collection_name=searchString,
                                                                query={'product_name': product_name})
                        print(db_search)
                        if db_search is not None:
                            print("Yes present" + str(len(db_search)))
                            continue
                        print("False")
                        product_searched = self.getProductSearched(search_string=searchString)
                        price = self.getPrice()
                        offer_details = self.getOfferDetails()
                        discount_percent = self.getDiscountedPercent()
                        EMI = self.getEMIDetails()
                        total_review_page = self.getTotalReviewPage()
                        count = 0
                        while count <= total_review_page:
                            if review_count > expected_review:
                                return search
                            count = count + 1
                            new_url = self.driver.current_url + "&page=" + str(count + 1)
                            for i in self.getReviewDetailsForProduct():
                                ratings = i[0][0]
                                comment = i[1][0]
                                customer_name = i[2][0]
                                review_age = i[3][0]
                            if len(ratings) > 0:
                                for i in range(0, len(ratings)):
                                    if review_count > expected_review: return search
                                    result = {'product_name': product_name,
                                              'product_searched': product_searched,
                                              'price': price,
                                              'offer_details': offer_details,
                                              'discount_percent': discount_percent,
                                              'EMI': EMI,
                                              'rating': ratings[i],
                                              'comment': comment[i],
                                              'customer_name': customer_name[i],
                                              'review_age': review_age[i]}
                                    mongoClient.insertRecord(db_name="Flipkart-Scrapper",
                                                             collection_name=searchString,
                                                             record=result)
                                    print(result)
                                    review_count = review_count + 1
                                    print(review_count)
                            self.openUrl(url=new_url)
            return search
        except Exception as e:
            raise Exception(f"(getReviewsToDisplay) - Something went wrong on yielding data.\n" + str(e))
