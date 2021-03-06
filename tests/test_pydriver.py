import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def test_execute_script(py):
    py.visit('https://google.com')
    webelement = py.get("[name='q']").webelement
    assert py.execute_script('return arguments[0].parentNode;', webelement)


def test_google_search(py):
    py.visit('https://google.com')
    py.get("[name='q']").type('puppies', Keys.ENTER)
    assert 'puppies' in py.title


def test_cookies(py):
    cookie_to_set = {'name': 'foo', 'value': 'bar'}
    cookie_to_test = {
        'domain': 'www.google.com',
        'httpOnly': False,
        'name': 'foo',
        'path': '/',
        'secure': True,
        'value': 'bar'
    }
    py.visit('https://google.com')

    py.set_cookie(cookie_to_set)
    assert py.get_cookie('foo') == cookie_to_test

    py.delete_cookie('foo')
    assert py.get_cookie('foo') is None


def test_viewport(py):
    py.visit('https://google.com')
    py.viewport(1280, 800)
    assert {'width': 1280, 'height': 800} == py.window_size


def test_find_single_element_with_xpath(py):
    py.visit('https://google.com')
    py.xpath('//*[@name="q"]').type('QA at the Point', Keys.ENTER)
    assert 'QA at the Point' in py.title


def test_find_elements_with_xpath(py):
    py.visit('https://deckshop.pro')
    assert py.xpath('//a[@class="nav-link"]').length > 1


def test_hover_and_click_to_page_transition(py):
    py.visit('https://qap.dev')
    py.get('a[href="/about"]').hover().get('a[href="/leadership"][class*=Header]').click()
    assert py.contains('Carlos Kidman').text == 'Carlos Kidman'


def test_pylenium_wait_until(py):
    py.visit('https://qap.dev')
    element = py.wait(use_py=True).until(lambda x: x.find_element_by_css_selector('[href="/about"]'))
    assert element.tag_name == 'a'
    assert element.hover()


def test_pylenium_wait_until_with_seconds(py):
    py.visit('https://qap.dev')
    py.wait(use_py=True).sleep(2)
    element = py.wait(5, use_py=True).until(lambda x: x.find_element_by_css_selector('[href="/about"]'))
    assert element.tag_name == 'a'
    assert element.hover()


def test_webdriver_wait_until(py):
    py.visit('https://qap.dev')
    element = py.wait(5).until(lambda x: x.find_element_by_css_selector('[href="/about"]'))
    assert element.tag_name == 'a'


def test_switch_to_frame_then_back(py):
    py.visit('http://the-internet.herokuapp.com/iframe')
    py.switch_to.frame('mce_0_ifr').get('#tinymce').clear().type('foo')
    assert py.switch_to.default_content().contains('An iFrame').tag_name == 'h3'
    py.switch_to.frame('mce_0_ifr').get('#tinymce').type('bar')
    assert py.get('#tinymce').text == 'foobar'
    assert py.switch_to.parent_frame().contains('An iFrame').tag_name == 'h3'
