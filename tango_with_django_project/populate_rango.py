import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'tango_with_django_project.settings')

import django 

django.setup()

from rango.models import Category, Page

def Populate() :

    python_pages = [
        {"title": "Official Python Tutorial",
        "url":"http://docs.python.org/2/tutorial/"},
        {"title":"How to Think like a Computer Scientist",
        "url":"http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/"} ]

    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/"} ]

    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
        "url":"http://flask.pocoo.org"} ]

    cats = {"Python": {"pages": python_pages,"views":128,"likes":64,},
        "Django": {"pages": django_pages,"views":64 ,"likes":32,},
        "Other Frameworks": {"pages": other_pages,"views":32,"likes":16,}, }


    # Loop to add categories and pages
    for cat, cat_data in cats.iteritems() :
        c = add_cat(cat,cat_data["views"],cat_data["likes"])
        for p in cat_data["pages"] :
            add_page(c,p["title"],p["url"])

    # to print
    for c in Category.objects.all() :
        for p in Page.objects.filter(category = c) :
            print("- {0} - {1} ".format(str(c),str(p)))
    
#Function to add page
def add_page(cat,title,url,views=0) :
    p = Page.objects.get_or_create(category = cat, title = title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

#Function to add category
def add_cat(name,views=0,likes=0) :
    c = Category.objects.get_or_create(name = name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c

#Execute
if __name__ == '__main__' :
    Populate()

    
