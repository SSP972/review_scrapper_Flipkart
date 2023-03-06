class ObjectRepository:

    def __init__(self):
        print()

    def getUsernameforMongoDB(self):
        username = "kavimaurya1997@gmail.com"
        return username

    def getPasswordforMongoDB(self):
        password = "Kavita@123"
        return password

    def getLoginCloseButton(self):
        login_close_button = "//body[1]/div[2]/div[1]/div[1]/button[1]"
        return login_close_button

    def getInputSearchArea(self):
        search_inputarea = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/div[1]/input[1]"
        return search_inputarea

    def getElementTobeSearched(self):
        element = "_10Ermr"
        return element

    def getSearchButton(self):
        search_button = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/form[1]/div[1]/button[1]"
        return search_button

    def getRatingandReviewsText(self):
        rating_and_review_text = "//div[contains(text(),'Ratings & Reviews')]"
        return rating_and_review_text

    def getProductNameByXpath(self):
        product_name = "//body[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/h1[1]/span[2]"
        return product_name

    def getProductNameByClass(self):
        product_name = "B_NuCI"
        return product_name

    def getProductSearchedByXpath(self):
        product_searched = "//body[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/h1[1]/span[1]"
        return product_searched

    def getProductSearchedByClass(self):
        product_searched = "G6XhRU"
        return product_searched

    def getOriginalPriceUsingClass(self):
        original_price = "_30jeq3"
        return original_price

    def getOriginalPriceUsingXpath(self):
        original_price = "//body[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]"
        return original_price

    def getDiscountPercent(self):
        discount_percent = "_3Ay6Sb"
        return discount_percent

    def getEMIDetail(self):
        emi_detail = "//body[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/span[3]/li[1]/span[1]"
        return emi_detail

    def getViewPlanLinkUsingClass(self):
        viewPlan = "_3IATq1"
        return viewPlan

    def getAvailableOffers(self):
        available_offers1 = "_3TT44I"
        available_offers2 = "WT_FyS"
        return available_offers1, available_offers2

    def getMoreOffers(self):
        more_offer = "IMZJg1"
        return more_offer

    def getMoreOffersUsingClass(self):
        more_offer = "IMZJg1 Okf99z"
        return more_offer

    def getRatings(self):
        rating = "div._3LWZlK._1BLPMq"
        return rating

    def getComment(self):
        comment1 = "_6K-7Co"
        comment2 = "_2-N8zT"
        return comment1,comment2

    def getCustomerName(self):
        comment_date = "_2sc7ZR"
        return comment_date

    def getTotalReviewPage(self):
        total_page_1 = "_2MImiq"
        #total_page_2 ="//body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[13]/div[1]/div[1]/span[1]"
        return total_page_1



#
    def getMoreReviewUsingClass(self):
        more_review_1 = "_3at_-o"
        more_review_2 = "_3UAT2v"
        return more_review_1, more_review_2
#
    def getNextFromTotalReviewPage(self):
        next_button = "_1LKTO3"
        return next_button

