html_example = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BeautifulSoup 활용</title>
</head>
<body>
    <h1 id="heading">Heading 1</h1>
    <p>Paragraph</p>
    <span class="red">BeautifulSoup Library Examples!</span>
    <div id="link">
        <a class="external_link" href="www.google.com">google</a>

        <div id="class1">
            <p id="first">class1's first paragraph</p>
            <a class="exteranl_link" href="www.naver.com">naver</a>

            <p id="second">class1's second paragraph</p>
            <a class="internal_link" href="/pages/page1.html">Page1</a>
            <p id="third">class1's third paragraph</p>
        </div>
    </div>
    <div id="text_id2">
        Example page
        <p>g</p>
    </div>
    <h1 id="footer">Footer</h1>
</body>
</html>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_example, 'html.parser')

print(soup.title)
print(soup.title.string)
print(soup.title.get_text())

print(soup.title.parent)

print(soup.body)
print()
print()
print(soup.h1)
print(soup.h1.string)
print()
print()
print(soup.a)
print(soup.a.string)
print(soup.a['href'])
print(soup.a.get('href'))

print(soup.find('div', {'id': 'text_id2'}))
print()
print()


div_text = soup.find('div', {'id' : 'text_id2'})
print(div_text.text)

print(div_text.string)

print()
print()

href_link = soup.find('a', {'class' : 'internal_link'})
href_link = soup.find('a', class_ = 'internal_link')

print(href_link)
print(href_link['href'])
print(href_link.get('href'))
print(href_link.text)
print()
print()

print('href_link.attrs: ', href_link.attrs)
print('class 속성값: ', href_link['class'])

print('values() : ', href_link.attrs.values())

values = list(href_link.attrs.values())
print(f"values[0] : {values[0]}, values[1] : {values[1]}")

href_value = soup.find(attrs = {'href' : 'www.google.com'})
href_value = soup.find('a', attrs = {'href' : 'www.google.com'})
print()
print()
print('href_value : ', href_value)
print(href_value['href'])
print(href_value.string)

print()
print()

span_tag = soup.find('span')

print('span tag : ', span_tag)
print('attrs : ', span_tag.attrs)
print('value : ', span_tag.attrs['class'])
print('text : ', span_tag.text)

print()
print()

div_tags = soup.find_all('div')
print('div_tags length : ', len(div_tags))

for div in div_tags:
    print('----------------------------------')
    print(div)


print()
print()

links = soup.find_all('a')

for alink in links:
    print(alink)
    print(f"url : {alink['href']}, text : {alink.string}")
    print()

link_tags = soup.find_all('a', {'class' : ['external_link', 'internal_link']})
print(link_tags)

p_tags = soup.find_all('p', {'id' : ['first', 'third']})
for p in p_tags:
    print(p)

print()
head = soup.select_one('head')
print(head)
print('head.text : ', head.text.strip())

print()
h1 = soup.select_one('h1')
print(h1)


footer = soup.select_one('h1#footer')
print(footer)

print()
print()
class_link = soup.select_one('a.internal_link')
print(class_link)

print(class_link.string)
print(class_link['href'])

print()
print()
link1 = soup.select_one('div#link > a.external_link')
print(link1)

link_find = soup.find('div', {'id' : 'link'})

external_link = link_find.find('a', {'class' : 'external_link'})
print('find external_link : ', external_link)
print()
print()

link2 = soup.select_one('div#class1 p#second')
print(link2)
print(link2.string)

print()
print()

internal_link = soup.select_one('div#link a.internal_link')
print(internal_link['href'])
print(internal_link.text)

print()
print()

h1_all = soup.select('h1')
print('h1_all: ', h1_all)

url_links = soup.select('a')
for link in url_links:
    print(link['href'])

print()
print()

div_urls = soup.select('div#class1 > a')

print(div_urls)
print(div_urls[0]['href'])

print()
print()

div_urls2 = soup.select('div#class1 a')
print(div_urls2)

print()
print()

h1 = soup.select('#heading, #footer')
print(h1)

print()

url_links = soup.select('a.external_link, a.internal_link')
print(url_links)