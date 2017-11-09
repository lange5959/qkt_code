def find(node):
    if node.type().name() == 'alembic':
        return [node]
    else:
        result = []
        for c in node.children():
            result.extend(find(c))
        return result
 # print find(hou.selectedNodes()[0])
def merge(objs):
    merge_node = hou.node('/obj').createNode('geo')
    merge_node.setName('merged', 1)
    merge_node.node('file1').destroy()
    merge_node.moveToGoodPosition()

    obj_merge_node = merge_node.createNode('object_merge')
    obj_merge_node.parm('xformtype').set(1)

    children_to_merge = []
    for obj in objs:
        children_to_merge.extend(find(obj))
    print '>'*15
    print children_to_merge
    obj_merge_node.parm('numobj').set(len(children_to_merge))

    for i,c in enumerate(children_to_merge):
        obj_merge_node.parm('objpath%i' % (i+1)).set(c.path())

merge(hou.selectedNodes())