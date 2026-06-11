class test_ast:
    def add_item(self,item, items=[]) -> list():
        items.append(item)
        return items
a=test_ast()
print(a.add_item(1)) 
print(a.add_item(2)) 
