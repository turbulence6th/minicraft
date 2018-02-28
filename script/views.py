from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
import minicraft
from minicraft.user import User
from minicraft.item import Item
import ConfigParser
import os
import ast

def login(request):
    if request.method == 'GET':
        pass


    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User(username, password) in User.userList:
            user = User.userList[User.userList.index(User(username, password))]
            if user.active:
                return HttpResponseRedirect("/")

            else:
                user.active = True
                request.session['username'] = user.username
                request.session['password'] = user.password
                minicraft.map.addObjectRandom(user)
                return HttpResponseRedirect("game")
        else:
            return HttpResponseRedirect("/")


    return render(request, 'script/login.html', {})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User(username, password) in User.userList:
            user = User.userList[User.userList.index(User(username, password))]
            if user.active:
                data = {'check': False}
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
				user.active = True
        else:
            user = User(username, password)
            User.userList.append(user)
            minicraft.map.addObjectRandom(user)

            data = {'check': True}
            request.session['username'] = user.username
            request.session['password'] = user.password
            return HttpResponse(json.dumps(data), content_type="application/json")

def game(request):
	print request.session['username']
	print request.session['password']
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map.map(user)

    Config = ConfigParser.ConfigParser()
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    Config.read(os.path.join(PROJECT_PATH, '../minicraft/config_merge'))

    targets_pre = Config.sections()

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    targets = []

    for i in targets_pre:
        isTrue = True
        ingr = ConfigSectionMap(i)
        for j in ingr:
            isTrue = isTrue and user.hasItems(Item(j, int(ingr[j])))
        if isTrue:
            targets.append(i)

    use = []
    for i in user.inventory:
        if i.handable:
            use.append(str(i.itemType))
    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__

    if user.handle:
        usage = user.handle.itemType
    else:
        usage = None
    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })

    return render(request, 'script/game.html', {'map': map, 'inventory_1': inventory_1,'inventory_2': inventory_2,
                    'targets': targets, 'use': use,'left': left, 'right': right, 'up': up, 'down': down, 'usage': usage,
                                                'is_target': targets != []})




def move(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map

    map.moveObject(user, request.POST.get('direction'))

    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__



    return HttpResponse(json.dumps({'map':map.map(user),'left': left,
            'right': right, 'up': up, 'down': down, }), content_type="application/json")

def acquire(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map

    map.acquireObject(user, request.POST.get('direction'))

    Config = ConfigParser.ConfigParser()
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    Config.read(os.path.join(PROJECT_PATH, '../minicraft/config_merge'))

    targets_pre = Config.sections()

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    targets = []

    for i in targets_pre:
        isTrue = True
        ingr = ConfigSectionMap(i)
        for j in ingr:
            isTrue = isTrue and user.hasItems(Item(j, int(ingr[j])))
        if isTrue:
            targets.append(i)

    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__

    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })


    return HttpResponse(json.dumps({'map':map.map(user), 'inventory_1': inventory_1,'inventory_2': inventory_2,
                    'targets': targets, 'left': left, 'right': right, 'up': up, 'down': down,
                                                'is_target': targets != [] }), content_type="application/json")

def damage(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map

    map.damage(user, request.POST.get('direction'))

    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__



    return HttpResponse(json.dumps({'map':map.map(user), 'left': left, 'right': right, 'up': up, 'down': down
                                                 }), content_type="application/json")


def eat(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    user.eat()
    map = minicraft.map.map(user)

    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })

    return HttpResponse(json.dumps({'inventory_1': inventory_1,'inventory_2': inventory_2, 'map': map
                     }), content_type="application/json")


def put(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map

    map.putObject(user, request.POST.get('direction'), Item(request.POST.get('item')) )

    map = minicraft.map.map(user)

    Config = ConfigParser.ConfigParser()
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    Config.read(os.path.join(PROJECT_PATH, '../minicraft/config_merge'))

    targets_pre = Config.sections()

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    targets = []

    for i in targets_pre:
        isTrue = True
        ingr = ConfigSectionMap(i)
        for j in ingr:
            isTrue = isTrue and user.hasItems(Item(j, int(ingr[j])))
        if isTrue:
            targets.append(i)

    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })

    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__

    use = []
    for i in user.inventory:
        if i.handable:
            use.append(str(i.itemType))
    if user.handle:
        usage = user.handle.itemType
    else:
        usage = None

    return HttpResponse(json.dumps({'map': map, 'inventory_1': inventory_1,'inventory_2': inventory_2,
                    'targets': targets, 'use': use,'left': left, 'right': right, 'up': up, 'down': down, 'usage': usage,
                                                'is_target': targets != []}), content_type="application/json")


def use(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    user.useItem(Item(request.POST.get('item')))

    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    use = []
    for i in user.inventory:
        if i.handable:
            use.append(str(i.itemType))
    if user.handle:
        usage = user.handle.itemType
    else:
        usage = None

    return HttpResponse(json.dumps({'inventory_1': inventory_1,'inventory_2': inventory_2,'use': use, 'usage': usage,
                     }), content_type="application/json")


def quit(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    user.active = False

    map = minicraft.map
    map.deleteObject(user)
    user.coordinate = None

    return HttpResponseRedirect("/")

def refresh(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    map = minicraft.map.map(user)

    coordinate = user.coordinate
    left = type(minicraft.map.getObject(coordinate.decX())).__name__
    up = type(minicraft.map.getObject(coordinate.decY())).__name__
    right = type(minicraft.map.getObject(coordinate.incX())).__name__
    down = type(minicraft.map.getObject(coordinate.incY())).__name__

    return HttpResponse(json.dumps({'map': map, 'left': left, 'right': right, 'up': up, 'down': down
                     }), content_type="application/json")

def tutorial(request):
    return render(request, 'script/tutorial.html',{})

def merge(request):
    user = User.userList[User.userList.index(User(request.session['username'], request.session['password']))]
    user.merge(request.POST.get('target'))

    Config = ConfigParser.ConfigParser()
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    Config.read(os.path.join(PROJECT_PATH, '../minicraft/config_merge'))

    targets_pre = Config.sections()

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    pass
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    targets = []

    for i in targets_pre:
        isTrue = True
        ingr = ConfigSectionMap(i)
        for j in ingr:
            isTrue = isTrue and user.hasItems(Item(j, int(ingr[j])))
        if isTrue:
            targets.append(i)

    use = []
    for i in user.inventory:
        if i.handable:
            use.append(str(i.itemType))


    inventory_1 = []
    inventory_2 = []
    for i in user.inventory[0:7]:
        inventory_1.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })
    for i in user.inventory[7:]:
        inventory_2.append({ 'itemType': i.itemType, 'count': i.count, 'handable': i.handable })

    return HttpResponse(json.dumps({'inventory_1': inventory_1,'inventory_2': inventory_2,
                    'targets': targets, 'is_target': targets != [], 'use': use }), content_type="application/json")








