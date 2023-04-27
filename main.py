import asyncio
from pyppeteer import launch


async def search_mobile(mobile):
    # 启动浏览器
    browser = await launch()
    page = await browser.newPage()

    # 访问百度搜索页面
    await page.goto('https://www.baidu.com/s?wd=' + mobile)

    # 画面截屏到本地
    # await page.screenshot({'path': 'test.png'})

    # 等待页面加载完毕
    await page.waitForSelector('#content_left')

    # 获取搜索结果列表
    result_list = await page.xpath('//div[@class="result-op c-container new-pmd" and @id="1"]')
    # print(result_list)

    # 遍历搜索结果，查找是否有标记信息
    for result in result_list:
        text = await page.evaluate('(element) => element.innerText', result)
        # print(text)
        if '骚扰电话' in text:
            print(mobile, '已被标记为骚扰电话')
            break
    else:
        print(mobile, '不是骚扰电话')

    # 关闭浏览器
    await browser.close()


# 测试代码
if __name__ == '__main__':
    mobile_list = ['03515646287', '13600136000', '13000130000']
    asyncio.get_event_loop().run_until_complete(asyncio.gather(*[search_mobile(mobile) for mobile in mobile_list]))
