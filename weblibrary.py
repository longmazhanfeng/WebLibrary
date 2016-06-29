# -*- coding: utf-8 -*-
import os
import time
from keywordgroup import KeywordGroup
from robot.api import logger
from selenium.webdriver.common.action_chains import ActionChains
try:
	import SendKeys
except ImportError:
	# try to import other lib for target OS platform
	pass
try:
	import win32gui
except ImportError:
	# try to import other lib for target OS platform
	pass

class _WebKeywords(KeywordGroup):

	# Public Web Keywords

	def web_hover_and_click(self, elementToHover_locator, elementToClick_locator):
		"""Hover and click

		(在运行该KW会将浏览器窗口移到你看不到的地方，以后也别想看到，屏幕截图是好的，哈哈~~)
		elementToHover_locator hover的区域位置，elementToClick_locator 要点击的元素位置
        | Web Hover And Click | ${elementToHover_locator} | ${elementToClick_locator} |
        | Web Hover And Click | locator1_hover | locator2_toclick |
		"""
		#self._current_browser().set_window_size(100, 100)#设置窗口大小
		self._current_browser().set_window_position(-10000, -10000)#设置窗口位置将窗口移出桌面。。。
		self._info("Hover '%s' and click '%s'" % (elementToHover_locator, elementToClick_locator))
		elementToHover = self._element_find(elementToHover_locator, True, False)
		elementToClick = self._element_find(elementToClick_locator, True, False)
		if elementToHover is None:
		    raise AssertionError("ERROR: Element %s not found." % (elementToHover_locator))
		if elementToClick is None:
			raise AssertionError("ERROR: Element %s not found." % (elementToClick_locator))
		actions = ActionChains(self._current_browser())
		actions.move_to_element(elementToHover)
		actions.click(elementToClick)
		actions.perform()
		self._current_browser().set_window_position(0, 0)#移回来了。。

	def web_upload_file(self, filepath):
		"""上传文件(用于flash上传控件)

		filepath 文件路径，支持绝对路径和相对路径，注意写法，例如：${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg
        ${CURDIR}指数据所在文件的当前路径
		RF中filepath的写法被认为是unicode
		另外，这里的输入依赖系统的输入法，建议提前切换至英文，用美式键盘最好
		| Web Upload File | ${filepath} |	
		| Web Upload File | ${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg | 	
		"""
		filepath=os.path.abspath(filepath)
		change = str(filepath)
		time.sleep(1)
		self._handle = win32gui.FindWindow(None, u"打开")#获取“打开”窗口的句柄
		win32gui.SetForegroundWindow(self._handle)#聚焦当前窗口
		SendKeys.SendKeys(change)
		time.sleep(1)
		SendKeys.SendKeys("{ENTER}")

	def web_click_element(self, locator, selected_num=1):
		"""点击元素操作（locator搜索结果为多个元素时，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        locator: 同Selenium2Library里的locator;
        selected_num: 指定元素序号.
        [不输入（默认值）:   点击第一个元素]
        [=0 :              点击最后一个元素]
        [=x（>0）:          点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Click Element | ${locator} | ${selected_num} |
		| Web Click Element | id=username | 2 |
	    locator 示例:
    	| identifier | Click Element `|` identifier=my_element | Matches by @id or @name attribute               |
    	| id         | Click Element `|` id=my_element         | Matches by @id attribute                        |
    	| name       | Click Element `|` name=my_element       | Matches by @name attribute                      |
    	| xpath      | Click Element `|` xpath=//div[@id='my_element'] | Matches with arbitrary XPath expression |
		"""		
		selected_element = self._get_selected_element(locator, selected_num)
		selected_element.click()


	def web_click_text_button(self, text, selected_num=1):
		"""点击可以通过按钮内文字定位的文本/按钮（Button/Link）元素（相同文字的按钮为多个元素时，默认点击其中第一个，可以设定target_num，点击指定第n元素）
        text: 为按钮内的文字, 比如： 欢迎页－登录平台  主菜单页－群发消息/分组管理
        target_num: 指定元素（按钮）序号
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		text 为按钮内的文字
		如下的控件可以使用：<a href="/mass">群发消息</a> 或 <input id="submit-button" type="button" class="submit u-btn" value="快速登录平台">
		<button>中&nbsp;文</button>
		| Web Click Text Button | ${text} | ${selected_num} |
		| Web Click Text Button | 群发消息 | 2 |
		| Web Click Text Button | 中&nbsp;文 |
		"""
		# change '&nbsp;' to unicode string '\u00a0'
		u_space = u"\u00a0"
		if h_space in text:
			text = text.replace(h_space, u_space)
		# common_locator = u"xpath=//*[contains(text(), '%s')]"  % text
		common_locator = u"xpath=//*[text()='%s']" % text
		if self.web_get_elements_num(common_locator) > 0:
			# 元素查询尝试1 text 方式： 所有标签（包括<a>标签 or 类<a>标签）的text值
			self.web_click_element(common_locator, selected_num)
		else:
			common_locator = "xpath=//*[@value='%s']" % text
			if self.web_get_elements_num(common_locator, timeout=1) > 0:
				# 元素查询尝试2 value属性 方式：所有标签 属性中的 value值
				self.web_click_element(common_locator, selected_num)
			else:
				# 元素查询尝试3 link 方式（自动过滤一些空格）
				common_locator = 'link=' + text	
				self.web_click_element(common_locator, selected_num)


	def web_input_text(self, locator, text, withenter='no'):
		"""向文本框中输入文本

		locator 同Selenium2Library里的locator
		text 用户名
		withenter 是否在最后按下Enter，默认是no
		| Web Input Text | ${locator} | ${text} |
		| Web Input Text | ${locator} | ${text} | ${withenter} |
		| Web Input Text | id=username | myaccount |
		| Web Input Text | id=username | myaccount | yes |
		"""
		self.wait_until_element_is_enabled(locator)
		self.input_text(locator, text)
		if withenter.lower() == 'yes':
			self.press_key(locator, '\\13')

	def web_input_password(self, locator, password):
		"""向文本框中输入密码

		locator 同Selenium2Library里的locator
		password 密码
		| Web Input Password | ${locator} | ${password} |
		| Web Input Password | id=password | mypassword |
		"""
		self.wait_until_element_is_enabled(locator)
		self.input_password(locator, password)

	def web_choose_file(self, locator, filepath):
		"""处理页面元素中input类型是file的元素，用来上传文件

		locator 同Selenium2Library里的locator
		filepath 文件路径，支持绝对路径和相对路径，注意写法
		| Web Choose File | ${locator} | ${filepath} |
		| Web Choose File | id=upload | ${CURDIR}${/}Res${/}Plus_Web${/}pic0.jpg |
		"""
		filepath=os.path.abspath(filepath)
		self.wait_until_element_is_enabled(locator)
		self.choose_file(locator, filepath)

	def web_click_chosen_element(self, locator, chosen_num=1):
		"""选择符合条件:locator定义的第chosen_num个元素，并点击它，与Web Click Element功能一致，推荐用Web Click Element

		locator 元素定位
		chosen_num 符合的第chosen_num个元素，默认是1，选取匹配的第一个元素
		| Web Click Chosen Element | ${locator} | ${chosen_num} |
		| Web Click Chosen Element | id=myid | 2 |
		"""
		selected_element = self._get_selected_element(locator, chosen_num)
		selected_element.click()

	def web_get_text(self, locator, selected_num=1):
		"""获取locator位置的text对应值（locator搜索结果为多个元素时，默认选择其中第一个，可以设定selected_num，指定第n元素）
        selected_num: 指定元素序号.
        [不输入（默认值）:  点击第一个元素]
        [=0 :             点击最后一个元素]
        [=x（>0）:         点击第x个元素]

		locator 同Selenium2Library里的locator
		| Web Get Text | ${locator} |
		| Web Get Text | id=myid |
		| ${button_num} | Web Get Text | id=myid |
		| ${button_num} | Web Get Text | xpath=//*[@class='col col-at j-number'] | 2 |
		"""
		element = self._get_selected_element(locator, selected_num)
		return element.text

	def web_get_elements_num(self, locator, timeout=None):
		"""返回符合locator定义的元素的个数 0-n
        locator: 同AppiumLibrary里的locator;

		| Web Get Elements Num | ${locator} |
		| Web Get Elements Num | id=myid |
		| ${element_num} | Web Get Elements Num | id=myid |
		"""		
		try:
			# self.wait_until_page_contains_element(locator, timeout)
			elements_list = self.get_webelements(locator)
		except Exception:
			#raise AssertionError("ERROR: Element %s not found." % (locator))
			return 0		
		return len(elements_list)

	def web_get_element_isDisplayed(self, locator):
		"""返回locator定位的元素是否可见，返回True或者false

		| Web Get Element IsDisplayed | ${locator} |
		| Web Get Element IsDisplayed | xpath=//div[@class='edit-btn'] |
		"""
		element = self._element_find(locator, True, False)
		return element.is_displayed()

	def web_get_text_button_num(self, text):
		"""返回匹配‘text’的文本/按钮（Button/Link）元素的个数 0-n
		text: 为按钮、Link元素内的文字, 比如： 登录  退出  查找

		| Web Get Text Button Num | ${text} |
		| Web Get Text Button Num | 登录 |
		| ${button_num} | Web Get Text Button Num | 15500000001 |
		| ${button_num} | Web Get Text Button Num | 登 录 |
		| ${button_num} | Web Get Text Button Num | 确 \ 认 |
		"""
        # 元素查询尝试1 text 方式： 所有标签（包括<a>标签 or 类<a>标签）的text值
		common_locator = "xpath=//*[text()='%s']" % text
		button_num = self.web_get_elements_num(common_locator)
		# 元素查询尝试2 value属性 方式（<a>标签 or 类<a>标签中的 value值）
		common_locator = "xpath=//*[@value='%s']" % text
		return button_num + self.web_get_elements_num(common_locator, timeout=1) 

	def _get_selected_element(self, locator, selected_num=1):
		"""返回选中的元素

		locator 元素位置
		selected_num 元素序号，从1开始
		"""
		# self.wait_until_page_contains_element(locator)
		self.wait_until_element_is_enabled(locator)
		index = int(selected_num) - 1
		elements_list = self.get_webelements(locator)
		if index < len(elements_list):
			return elements_list[index]
		else:			
			raise AssertionError("ERROR: Element selected_num %d is out of the length of elements_list" % int(selected_num))
