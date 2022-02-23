import imp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from linqit import List
from tabulate import tabulate

s = Service(ChromeDriverManager().install())
op = webdriver.ChromeOptions()
op.add_argument(r"start-maximized")
# op.add_experimental_option("detach", True);
driver = webdriver.Chrome(service=s, options=op)
driver.maximize_window()

# Mo trang Covid-19 cua Bo y te
driver.get(r"https://covid19.gov.vn/")
sleep(3)

# Chuyen sang frame co chua thong tin ve so ca Covid-19 cac tinh thanh
thongKeTinhThanhIframe = driver.find_element(
    By.XPATH, r'//*[@id="chartCovidStatistics"]/iframe')
driver.switch_to.frame(thongKeTinhThanhIframe)

# Lay so lieu tung row trong bang du dieu, ke ca dong tieu de


def LaySoLieuDongTrongBang(dongDuLieuWebElement):
    duLieuTinhThanhText = dongDuLieuWebElement.find_element(
        By.CLASS_NAME, r'city').text
    duLieuTongSoCaText = dongDuLieuWebElement.find_element(
        By.CLASS_NAME, r'total').text
    duLieu24GioQuaText = dongDuLieuWebElement.find_element(
        By.CLASS_NAME, r'daynow').text
    duLieuTuVongText = dongDuLieuWebElement.find_element(
        By.CLASS_NAME, r'die').text
    rowData = [duLieuTinhThanhText, duLieuTongSoCaText,
               duLieu24GioQuaText, duLieuTuVongText]
    return rowData

# Chuyen so lieu tu dang string sang dang so


def ChuyenDuLieuStringDongSangDuLieuInt(rowData):
    tongSoCaInt = int(str(rowData[1]).replace(".", ""))
    s24GioQuaString = str(rowData[2]).replace(".", "").replace("+", "").replace("-", "");
    i24GioQuaInt = int(s24GioQuaString) if s24GioQuaString else 0;
    tuVongInt = int(str(rowData[3]).replace(".", ""))
    return [rowData[0], tongSoCaInt, i24GioQuaInt, tuVongInt]


# Lay tieu de cac truong thong tin
dongTieuDeThongKe = driver.find_element(
    By.XPATH, r'//*[@id="location"]/div/div[1]')
header = LaySoLieuDongTrongBang(dongTieuDeThongKe)
# print(header);

# Lay so lieu thong ke cac tinh thanh
bangChuaDuLieuThongKe = driver.find_element(
    By.XPATH, r'//*[@id="location"]/div/div[2]')
cacDongChuaDuLieuThongKe = List(
    bangChuaDuLieuThongKe.find_elements(By.CLASS_NAME, r'row'))
duLieuThongKeCacTinhThanh = cacDongChuaDuLieuThongKe.select(
    lambda x: LaySoLieuDongTrongBang(x)).select(lambda y: ChuyenDuLieuStringDongSangDuLieuInt(y))
# print(duLieuThongKeCacTinhThanh);

# Hien thi du lieu ra console
print(tabulate(duLieuThongKeCacTinhThanh, headers=header))

driver.close()
