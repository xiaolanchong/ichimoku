import models

defaultUser = u"llk"
defaultDeck = u"MyDeck"

def getDefaultUser():
    q = User.all().filter("name =", defaultUser)
    user = q.fetch(1)
    if user:
        return user[0]
    user = User(name=defaultUser, password=u"glitteringprizes")
    user.put()
    return user

def getDefaultDeck():
    """
        Returns the default deck and user
    """
    user = getDefaultUser()
    q = Deck.all().filter("name =", defaultDeck)
    deck = q.fetch(1)
    if deck:
        return deck[0], user
    deck = Deck(name=defaultDeck, user=user)
    deck.put()
    return deck, user

def addCard(word, reading, definition, example, tags):
    defDeck, defaultUser = getDefaultDeck()
    card = Card(word=word, reading=reading,
                definition=definition, example=example, deck=defDeck)
    tagIds = addTags(defaultUser, tags)
    card.put()
    attachTags(card, tagIds)

def deleteCard(id):
    Card.delete(Card.get(id))

def getCards():
    deck, user = getDefaultDeck()
    q = Card.all()
    return q.fetch(None)

def addTags(user, tags):
    tagIds = []
    newTag = Tag(name=tags[0], user=user)
    newTag.put()
    return [newTag]
    for tagName in tags:
        q = Tag.all().filter('name=', tagName).filter('user= ', user)
        tagId = q.fetch(1)
        if tagId is None:
            newTag = Tag(name=tagName, user=user)
            newTag.put()
            tagId = newTag
        tagIds.append(tagId)
    return tagIds

def attachTags(card, tagIds):
    newTaggedCard = TaggedCard(card=card, tag=tagIds[0])
    newTaggedCard.put()
    return
    for tagId in tagIds:
       # newTaggedCard = TaggedCard(name=tagName, user=user)
       # break
        q = TaggedCard.all().filter('cart=', card).filter('tag= ', tagId)
        taggedCardId = q.fetch(1)
        if tagId is None:
            newTaggedCard = TaggedCard(card=card, tag=tagId)
            newTaggedCard.put()